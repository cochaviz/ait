#!/usr/bin/env python3

import argparse
import os
import io
import yaml
import re
import subprocess
import shlex

import logging
import glob


def _open_file(filename: str | None, programs: list[str] = ["code", "xdg-open"]):
    if filename is None:
        logging.info("Given filename was 'None'.")
        return

    for program in programs:
        try:
            return subprocess.run([program, filename], check=True).returncode
        except subprocess.CalledProcessError:
            continue

    logging.warning(
        f"open_file: Could not open file {filename} with any of the following programs: {programs}."
    )
    return 1


def _set_verbosity(level: str):
    numeric_level = getattr(logging, level.upper(), "WARNING")

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level}")

    logging.basicConfig(level=numeric_level)


def _docker_in_container_warning(docker_option: bool) -> None:
    if os.path.exists("/.dockerenv") and docker_option:
        logging.warning(
            """docker: Docker option seems to be enabled inside a
                            docker container. If you're in a docker container,
                            consider omitting this option."""
        )


def _open_metadata(path: str) -> dict[str, str] | None:
    assert os.path.isdir(path)  # should not trigger

    # open the
    with io.open(f"{path}/metadata.yaml", "r") as stream:
        metadata = yaml.safe_load(stream)
        return metadata


def _open_frontmatter(path: str) -> dict[str, str] | None:
    if os.path.isdir(path):
        raise ValueError("Dirs do not have frontmatters")

    import frontmatter

    if not frontmatter.checks(path):
        raise AttributeError("File does not contain frontmatter")

    return frontmatter.load(path).keys()  # type: ignore


def _get_metadata(path: str, property: str) -> str | None:
    search_dir = path + "/" if os.path.isdir(path) else os.path.dirname(path) + "/"
    metadata = None

    # first try getting the metadata.yaml file
    try:
        metadata = _open_metadata(search_dir)
    except FileNotFoundError as e:
        logging.info(f"metadata: Could not find metadata.yaml in folder {search_dir}")

    # then look for frontmatter
    try:
        metadata = _open_frontmatter(path)
    except ValueError:
        logging.info(f"frontmatter: {path} is not a file")
    except ImportError:
        logging.warning(
            f"frontmatter: Module 'frontmatter' not installed, cannot read frontmatter from {path}"
        )
    except FileNotFoundError:
        logging.warning(f"frontmatter: Could not find file {path}")
    except AttributeError:
        logging.info(f"frontmatter: File {path} does not contain frontmatter")

    # if we have a metadata file and are looking for a specific property
    if metadata is not None:
        try:
            return metadata[property]
        except KeyError:
            logging.error(
                f"metadata: Property {property} could not be found in metadata"
            )


def _title_to_filename(title: str):
    # keep alphanumeric
    filename = "".join(c for c in title if (c.isalnum() or c == " "))
    # remove any spaces and replace with underscore
    filename = re.sub("\ +", "_", filename)
    # make lowercase
    filename = filename.lower()

    return filename


def _determine_target_file_name(source_files, target):
    if "." in target:
        return target

    document_title = _get_metadata(source_files[0], "title")

    if document_title is not None:
        return f"{_title_to_filename(document_title)}.{target}"

    intermediate_filename = os.path.basename(
        os.path.dirname(source_files[0]) if len(source_files) > 1 else source_files[0]
    )
    return f"{os.path.splitext(intermediate_filename)[0]}.{target}"


def pandoc_run(
    pandoc: list[str], options: list[str], source_files: list[str], target: str
) -> tuple[str, subprocess.CompletedProcess]:
    out_filename = _determine_target_file_name(source_files, target)
    logging.info(f"Writing to {out_filename}...")

    return out_filename, subprocess_run_info(
        [
            *pandoc,
            *options,
            *source_files,
            f"--output={out_filename}",
        ]
    )


def subprocess_run_info(command: list[str], *args) -> subprocess.CompletedProcess:
    command_string = " ".join(command)
    logging.debug(f"build: Running command:\n----\n{command_string}\n----")
    return subprocess.run(command, *args)


def options_source_markdown(source, source_files, target) -> list[str]:
    options = [
        "--from=markdown+mark",
        "--filter=pandoc-crossref",
        "--citeproc",
        "--metadata=codeBlockCaptions",
    ]

    if os.path.exists(f"{source}/metadata.yaml"):
        options.append(f"--metadata-file={source}/metadata.yaml")
    if len(source_files) == 1 and "md" not in target:
        options.append(f"--shift-heading-level=-1")
    if "md" in target:
        options.append("--to=gfm")
    if "tex" in target:
        options.append("--standalone")

    return options


def build(
    source: str,
    target: str,
    options: list[str] = [],
    docker: bool = False,
    pandoc: str = "pandoc",
    tectonic: bool = False,
    open_file: bool = True,
    **_, # throw away all other added arguments
):  
    pandoc: list[str] = [pandoc]

    if docker:
        _docker_in_container_warning(docker)
        pandoc = shlex.split(
            f"docker run \
            --user {os.getuid()}:{os.getgid()} \
            --mount type=bind,source={os.getcwd()},target=/var/data \
            --workdir=/var/data \
            zoharcochavi/academic-markdown"
        )

    # source always refers to the folder which is being built
    if os.path.isdir(source):
        source_files = glob.glob(f"{source}/*.md")

        # if no files found, we cannot convert
        if len(source_files) == 0:
            logging.critical(
                f"build: No markdown files can be found in directory '{source}/'.\
                \nEither declare the specific file you want to convert, or select a different folder."
            )
            exit(1)
    else:
        source_files = [source]
        source = os.path.dirname(source)

    # all resources should be located in the source folder
    options.append(f"--resource-path={source}")

    # set options
    if "tex" in source_files[0]:
        logging.info("Using latex defaults")
        # options.append("--defaults=config/latex.yaml")
    elif "md" in source_files[0]:
        options += options_source_markdown(source, source_files, target)
    else:
        logging.error(
            f"build: It seems like you are trying to convert one or multiple non-latex/markdown files: {source_files}"
        )

        if not input(
            "Are you sure you want to build a non-latex/markdown file? [y/N]:"
        ).lower() in {
            "y",
            "yes",
        }:
            logging.warning("Not processing further, exiting...")
            exit(0)

    # if docker is used, set tectonic option by default
    if (tectonic or docker) and "pdf" in target:
        options.append("--pdf-engine=tectonic")

    out_filename = None
    returncode = 0

    # if there is a metadata.yaml file, treat as collective document
    if os.path.exists(f"{source}/metadata.yaml"):
        out_filename, process = pandoc_run(pandoc, options, source_files, target)
        returncode += process.returncode
    # otherwise render each separately
    else:
        for source_file in source_files:
            out_filename, process = pandoc_run(pandoc, options, [source_file], target)
            returncode += process.returncode

    if returncode != 0:
        logging.critical(f"pandoc: Exited unexpectedly.")
        exit(returncode)

    if open_file:
        _open_file(out_filename)


def check_health(docker: bool = False, **_):  # throw away all other added arguments
    health_check = ["./scripts/check_health.sh"]

    if docker:
        health_check.append("--docker")

    exit(subprocess.run(health_check).returncode)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="academic_markdown.py",
        description="""Wrapper for `pandoc` providing sensible
                                     defaults for rendering from pandoc-flavored
                                     markdown used in academic writing. Also
                                     performs other features related to writing and
                                     configuring""",
    )

    parser.add_argument(
        "--verbosity",
        type=str,
        choices=["ERROR", "WARNING", "INFO", "DEBUG"],
        default="WARNING",
        help="""Set verbosity level. Default is WARNING.""",
    )
    commands = parser.add_subparsers(required=True, title="commands")

    # build
    build_command = commands.add_parser(
        "build",
        description="Build document or set of documents through pandoc.",
        help="Command for building files and folders.",
    )
    build_command.add_argument(
        "source",
        help="""Source file or folder. In the case that the source is
                             a single file.""",
    )
    build_command.add_argument(
        "target",
        help="""Target output file, or extension (pdf, md, tex, etc.). Uses
                             pandoc under the hood, so refer to their documentation
                             for the options.""",
    )
    build_command.add_argument(
        "--options",
        default="",
        type=list[str],
        help="""Additional options to pass through to pandoc.""",
    )
    build_command.add_argument(
        "--pandoc",
        default="pandoc",
        type=str,
        help="""Path to pandoc in case it cannot be provided through the
                             PATH variable. Gets overridden if the --docker option is
                             set.""",
    )
    build_command.add_argument(
        "--docker",
        action="store_true",
        help="""Use docker configuration to build, requires docker to
                             be installed.""",
    )
    build_command.add_argument(
        "--check-health",
        action="store_true",
        help="""Check if dependencies are installed. If docker
                             flag is set, it will only check whether docker
                             requirement are met.""",
    )
    build_command.add_argument(
        "--do-not-open",
        action="store_false",
        help="""Do not open output in default code.""",
    )
    build_command.add_argument(
        "--tectonic",
        action="store_true",
        help="""Use tectonic when creating PDFs to install
                             missing packages on the fly. Is ignored when docker is
                             used.""",
    )
    build_command.set_defaults(command=build)

    # check health
    check_health_command = commands.add_parser(
        "check-health",
        description="""Check if all the necessary
                                           executables are available and properly configured.""",
        help="Command for determining the health of the setup.",
    )
    check_health_command.add_argument(
        "--docker", action="store_true", help="""Check Docker setup"""
    )
    check_health_command.set_defaults(command=check_health)

    # execute
    args = parser.parse_args()

    _set_verbosity(args.verbosity)
    logging.debug("Debugging 🤓")

    args.command(**args.__dict__)
