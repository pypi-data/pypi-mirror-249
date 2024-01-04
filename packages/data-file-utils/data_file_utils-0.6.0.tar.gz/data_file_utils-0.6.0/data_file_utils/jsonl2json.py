"""Parse JSONL file and write multiple JSON files."""
import json
import os
import sys
import click
import pathlib
import json
import logging
import pathlib

from typing import Dict
from datetime import datetime
from rich.console import Console


DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)


DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()


def parse_jsonl(input_file: str, output_folder: str) -> None:
    """Parse the JSONL file and write JSON files for each line.

    Args:
        input_file (str): the file path for the input JSONL file
        output_folder (str): the output directory where the JSON files will be written to
    """
    with open(input_file, 'r') as jsonl_file:
        for line_number, line in enumerate(jsonl_file, start=1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON at line {line_number}: {e}")
                continue

            output_file_path = os.path.join(output_folder, f"output_{line_number}.json")
            with open(output_file_path, 'w') as output_file:
                json.dump(data, output_file, indent=2)

            print(f"Processed line {line_number}. Output written to {output_file_path}")

def check_infile_status(infile: str = None, extension: str = None) -> None:
    """Check if the file exists, if it is a regular file and whether it has content.

    Args:
        infile (str): the file to be checked

    Raises:
        None
    """

    error_ctr = 0

    if infile is None or infile == '':
        error_console.print(f"'{infile}' is not defined")
        error_ctr += 1
    else:
        if not os.path.exists(infile):
            error_ctr += 1
            error_console.print(f"'{infile}' does not exist")
        else:
            if not os.path.isfile(infile):
                error_ctr += 1
                error_console.print(f"'{infile}' is not a regular file")
            if os.stat(infile).st_size == 0:
                error_console.print(f"'{infile}' has no content")
                error_ctr += 1
            if extension is not None and not infile.endswith(extension):
                error_console.print(f"'{infile}' does not have filename extension '{extension}'")
                error_ctr += 1

    if error_ctr > 0:
        error_console.print(f"Detected problems with input file '{infile}'")
        sys.exit(1)


@click.command()
@click.option('--logfile', help="Optional: The log file")
@click.option('--infile', help="Required: The input JSONL file (.jsonl)")
@click.option('--outdir', help="Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(logfile: str, infile: str, outdir: str, verbose: bool):
    """Parse JSONL file and write multiple JSON files."""
    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        error_console.print("Required command-line arguments were not provided")
        sys.exit(1)

    check_infile_status(infile, "jsonl")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")

    # Set the root logger
    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    parse_jsonl(infile, outdir)

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()
