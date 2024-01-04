import json
import signal
import sys
from pathlib import Path

from alive_progress import config_handler
from loguru import logger
from pydantic import ValidationError
from rich.traceback import install

from .config import get_config, get_dump_failed_posts, read_config
from .nyuu import Nyuu
from .parpar import ParPar
from .resume import Resume
from .utils import (
    delete_files,
    filter_empty_files,
    filter_par2_files,
    get_bdmv_discs,
    get_files,
    get_glob_matches,
    map_file_to_pars,
    move_files,
)
from .version import get_version

# Supress keyboardinterrupt traceback because I hate it
signal.signal(signal.SIGINT, lambda x, y: sys.exit(1))

# Install rich traceback
install()

# Set up logger
logger = logger.opt(colors=True)


def juicenet(
    path: Path,
    conf_path: Path,
    public: bool,
    only_nyuu: bool,
    only_parpar: bool,
    only_raw: bool,
    skip_raw: bool,
    clear_raw: bool,
    glob: list[str],
    bdmv: bool,
    debug: bool,
    move: bool,
    only_move: bool,
    extensions: list[str],
    no_resume: bool,
    clear_resume: bool,
) -> None:
    """
    Do stuff here
    """

    # Configure logger
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    level = "DEBUG" if debug else "INFO"
    logger.remove(0)
    logger.add(sys.stderr, format=fmt, level=level)

    # Progress bar config
    # Disable progress bar if --debug is used
    config_handler.set_global(length=50, theme="classic", dual_line=True, disable=debug)

    # Read config file
    try:
        conf_path = get_config(conf_path)
        conf_data = read_config(conf_path)
    except FileNotFoundError as error:
        logger.error(f"Config file not found: {error.filename}")
        sys.exit()
    except ValidationError as errors:
        logger.error(f"{errors.error_count()} errors in {conf_path.name}")
        for err in errors.errors():
            logger.error(f"{err.get('loc')[0]}: {err.get('msg')}")  # type: ignore
        sys.exit()

    # Get the values from config
    nyuu_bin = conf_data.NYUU.resolve()
    parpar_bin = conf_data.PARPAR.resolve()
    priv_conf = conf_data.NYUU_CONFIG_PRIVATE
    pub_conf = conf_data.NYUU_CONFIG_PUBLIC or priv_conf
    nzb_out = conf_data.NZB_OUTPUT_PATH.resolve()
    exts = extensions or conf_data.EXTENSIONS
    parpar_args = conf_data.PARPAR_ARGS

    appdata_dir = conf_data.APPDATA_DIR_PATH.resolve()
    appdata_dir.mkdir(parents=True, exist_ok=True)
    resume_file = appdata_dir / "juicenet.resume"
    resume_file.touch(exist_ok=True)

    if conf_data.USE_TEMP_DIR:
        work_dir = conf_data.TEMP_DIR_PATH
    else:
        work_dir = None

    # Decide which config file to use
    configurations = {"public": pub_conf.resolve(), "private": priv_conf.resolve()}
    scope = "public" if public else "private"
    conf = configurations[scope]

    # Check and get `dump-failed-posts` as defined in Nyuu config
    try:
        dump = get_dump_failed_posts(conf)
    except json.JSONDecodeError as error:
        logger.error(error)
        logger.error("Please check your Nyuu config and ensure it is valid")
        sys.exit()
    except KeyError as key:
        logger.error(f"{key} is not defined in your Nyuu config")
        sys.exit()
    except FileNotFoundError as error:
        logger.error(f"No such file: {error.filename}")
        sys.exit()

    logger.debug(f"Version: {get_version()}")
    logger.info(f"Config: {conf_path}")
    logger.info(f"Nyuu: {nyuu_bin}")
    logger.info(f"ParPar: {parpar_bin}")
    logger.info(f"Nyuu Config: {conf}")
    logger.info(f"NZB Output: {nzb_out}")
    logger.info(f"Raw Articles: {dump}")
    logger.info(f"Appdata Directory: {appdata_dir}")
    logger.info(f"Working Directory: {work_dir or path}")

    if glob or bdmv:
        logger.info(f"Glob Pattern: {glob or ['*/']}")
    else:
        logger.info(f"Extensions: {exts}")

    # --clear-raw
    if clear_raw:
        raw = get_glob_matches(dump, ["*"])
        count = len(raw)
        delete_files(raw)
        logger.info(f"Deleted {count} raw articles(s)")
        sys.exit()

    # Initialize Resume class
    resume = Resume(resume_file, scope, no_resume)

    # Initialize ParPar class for generating par2 files ahead
    parpar = ParPar(parpar_bin, parpar_args, work_dir, debug)

    # Initialize Nyuu class for uploading stuff ahead
    nyuu = Nyuu(path, nyuu_bin, conf, work_dir, nzb_out, scope, debug, resume, bdmv)

    if clear_resume:  # --clear-resume
        resume.clear_resume()  # Delete resume data
        sys.exit()

    # Check if there are any raw files from previous runs
    raw_count = len(get_glob_matches(dump, ["*"]))

    # --only-raw
    if only_raw:
        if raw_count != 0:
            nyuu.repost_raw(dump)
        else:
            logger.info("No raw articles available for reposting")
        sys.exit()

    if path.is_file():  # juicenet "file.mkv"
        files = [path]

    elif bdmv:  # --bdmv
        pattern = glob if glob else ["*/"]
        files = get_bdmv_discs(path, pattern)

    elif glob:  # --glob
        try:
            files = get_glob_matches(path, glob)
        except NotImplementedError as error:
            logger.error(error)
            sys.exit()
    else:
        files = get_files(path, exts)

    # Remove any par2 files present in the input
    # trying to run ParPar on a par2 file doesn't go well
    files = filter_par2_files(files)

    if not files:
        logger.error("No matching files/folders found in:")
        logger.error(path)
        sys.exit()

    if only_move:  # --only-move
        logger.info("Moving file(s)")
        move_files(files)
        logger.success("File(s) moved successfully")
        sys.exit()

    if move:  # --move
        logger.info("Moving file(s)")
        move_files(files)
        logger.success("File(s) moved successfully")

        # Get the new path of files
        files = get_files(path, exts)

    total = len(files)
    logger.debug(f"Total files: {total}")

    # Filter out empty paths and remove anything that isn't a directory or file
    files = filter_empty_files(files)

    non_empty_count = len(files)
    logger.debug(f"Empty files: {total-non_empty_count}")
    logger.debug(f"Total files left: {non_empty_count}")

    if not files:
        logger.error(
            "Matching files/folders found, but they are either empty or "
            "contain only 0-byte files, making them effectively empty"
        )
        sys.exit()

    files = resume.filter_uploaded_files(files)

    if not files:
        logger.info(
            "Matching files/folders found, but they were already uploaded before. "
            "You can force upload these with --no-resume"
        )
        sys.exit()

    if only_parpar:  # --parpar
        logger.debug("Only running ParPar")
        # If you're using parpar only then you probably don't want it going in temp
        parpar.workdir = None  # Generate par2 files next to the input files
        parpar.generate_par2_files(files)
        sys.exit()

    if only_nyuu:  # --nyuu
        logger.debug("Only running Nyuu")
        # Try to find any pre-existing `.par2` files
        mapping = map_file_to_pars(None, files)
        # Same logic as for --parpar
        nyuu.workdir = None
        nyuu.upload(mapping)
        sys.exit()

    if skip_raw:  # --skip-raw
        logger.warning("Raw article checking and reposting is being skipped")
        mapping = parpar.generate_par2_files(files)
        nyuu.upload(mapping)
        sys.exit()

    else:  # default
        if raw_count != 0:
            nyuu.repost_raw(dump)

        mapping = parpar.generate_par2_files(files)
        nyuu.upload(mapping)
