import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from alive_progress import alive_it
from loguru import logger

from .enums import BarTitle, CurrentFile
from .resume import Resume
from .utils import delete_files, get_glob_matches


class Nyuu:
    """
    A class representing Nyuu.

    Attributes:
        - `path (Path)`: The path to the directory containing the files to be uploaded.
        - `bin (Path)`: The path to Nyuu binary.
        - `conf (Path)`: The path to the Nyuu's configuration file.
        - `workdir (Optional[Path])`: Path to the directory for Nyuu execution and nzb file generation.
        - `outdir (Path)`: The path to the output directory where nzbs will end up after completion.
        - `scope (str)`: The scope of the nzbs made by Nyuu (Private or Public).
        - `debug (bool)`: Debug mode for extra logs.
        - `resume (Resume)`: Resume class for logging uploaded files.
        - `bdmv_naming (bool)`: Use alternate naming for the output nzbs if they are BDMV discs.

    Methods:
        - `move_nzb(file: Path, basedir: Path, nzb: str) -> None`: Move NZB to a specified output
           path in a somewhat sorted manner.
        - `cleanup(par2_files: list[Path]) -> None`: Cleans up par2 files after they are uploaded.
        - `upload(files: dict[Path, list[Path]]) -> None`: Uploads files to Usenet with Nyuu.
        - `repost_raw(dump: Path) -> None`: Tries to repost failed articles from the last run.

    This class is used to manage the uploading and reposting of files to Usenet using Nyuu.
    """

    def __init__(
        self,
        path: Path,
        bin: Path,
        conf: Path,
        workdir: Optional[Path],
        outdir: Path,
        scope: str,
        debug: bool,
        resume: Resume,
        bdmv_naming: bool,
    ) -> None:
        self.path = path
        self.bin = bin
        self.conf = conf
        self.workdir = workdir
        self.outdir = outdir
        self.scope = scope
        self.debug = debug
        self.resume = resume
        self.bdmv_naming = bdmv_naming

    def move_nzb(self, file: Path, basedir: Path, nzb: str) -> None:
        """
        Move NZB to a specified output path in a somewhat sorted manner
        """
        # self.path = /data/raven/videos/show/
        # file = /data/raven/videos/show/extras/specials/episode.mkv
        subdir = file.relative_to(self.path)  # /extras/specials/episode.mkv
        subdir = subdir.parent  # /extras/specials/

        src = self.workdir / nzb if self.workdir else basedir / nzb
        dst = self.outdir / self.scope / self.path.name / subdir  # ./out/private/show/extras/specials/
        dst.mkdir(parents=True, exist_ok=True)
        dst = dst / nzb  # ./out/private/show/extras/specials/episode.mkv.nzb
        shutil.move(src, dst)  # ./workdir/01.nzb -> ./out/private/show/extras/specials/episode.mkv.nzb

        logger.debug(f"NZB Move: {src} -> {dst}")

    def upload(self, files: dict[Path, list[Path]]) -> None:
        """
        Upload files to Usenet with Nyuu
        """
        sink = None if self.debug else subprocess.DEVNULL

        keys = files.keys()
        bar = alive_it(keys, title=BarTitle.NYUU)

        for key in bar:
            nzb = f"{key.name}.nzb".replace("`", "'")  # Nyuu doesn't like backticks

            if self.bdmv_naming:
                parent = key.relative_to(self.path).parent.name.replace("`", "'")
                if parent:
                    nzb = f"{parent}_{nzb}"

            nyuu = [self.bin] + ["--config", self.conf] + ["--out", nzb] + [key] + files[key]

            logger.debug(shlex.join(str(arg) for arg in nyuu))
            bar.text(f"{CurrentFile.NYUU} {key.name} ({self.scope})")

            cwd = self.workdir if self.workdir else key.parent  # this is where nyuu will be executed
            subprocess.run(nyuu, cwd=cwd, stdout=sink, stderr=sink)  # type: ignore

            # move completed nzb to output dir
            self.move_nzb(key, cwd, nzb)

            # save file info to resume data
            self.resume.log_file_info(key)

            # Cleanup par2 files for the uploaded file
            delete_files(files[key])

    def repost_raw(self, dump: Path) -> None:
        """
        Try to repost failed articles from last run
        """
        sink = None if self.debug else subprocess.DEVNULL

        articles = get_glob_matches(dump, ["*"])
        raw_count = len(articles)
        logger.info(f"Found {raw_count} raw articles. Attempting to repost")

        bar = alive_it(articles, title=BarTitle.RAW)

        for article in bar:
            nyuu = (
                [self.bin]
                + ["--config", self.conf]
                + [
                    "--skip-errors",
                    "all",
                    "--delete-raw-posts",
                    "--input-raw-posts",
                    article,
                ]
            )

            bar.text(f"{CurrentFile.RAW} {article.name}")
            logger.debug(shlex.join(str(arg) for arg in nyuu))

            subprocess.run(nyuu, cwd=self.path, stdout=sink, stderr=sink)  # type: ignore

        raw_final_count = len(get_glob_matches(dump, ["*"]))
        if raw_final_count == 0:
            logger.success("All raw articles reposted")
        else:
            logger.info(f"Reposted {raw_count-raw_final_count} articles")
            logger.warning(f"Failed to repost {raw_final_count} articles. Either retry or use --clear-raw")
