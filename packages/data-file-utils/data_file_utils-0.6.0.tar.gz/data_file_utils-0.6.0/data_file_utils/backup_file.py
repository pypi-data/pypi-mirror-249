"""Backup a file."""
import logging
import os
import sys
import click
import pathlib
import logging
import pathlib
import shutil

from pathlib import Path

from datetime import datetime
from rich.console import Console

from .file_utils import check_infile_status

DEFAULT_TIMESTAMP = str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))


DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()


@click.command()
@click.argument('infile', type=str, required=True)
def main(infile: str):
    """Backup a file in-place."""

    error_ctr = 0

    if infile is None:
        error_console.print(f"Usage: {os.path.basename(__file__)} infile")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    check_infile_status(infile)

    dirname = os.path.dirname(infile)
    bakfile = os.path.join(
        dirname,
        os.path.basename(infile) + f".{DEFAULT_TIMESTAMP}.bak"
    )

    shutil.copyfile(infile, bakfile)
    print(f"Backed-up '{infile}' to '{bakfile}'")


if __name__ == "__main__":
    main()
