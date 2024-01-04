import csv
import logging
import os
import os
import sys
import click
import pathlib
import json
import logging
import calendar
import time
import pathlib
import yaml
from pathlib import Path

from typing import Any, Dict

from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

DEFAULT_HEADER_LINE = 1
DEFAULT_START_LINE = 2
DEFAULT_INCLUDE_LINE_NUMBERS = False

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'conf',
    'config.yaml'
)

CONFIG = {}

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()



def convert_file(
    infile: str,
    outfile: str,
    header_line: int = DEFAULT_HEADER_LINE,
    start_line: int = DEFAULT_START_LINE,
    include_line_numbers: bool = DEFAULT_INCLUDE_LINE_NUMBERS
) -> None:


    record_lookup = get_record_lookup(infile, header_line, start_line, include_line_numbers)
    # Write the list of ordered dictionaries to a JSON file
    lookup = {
        "infile": os.path.abspath(infile),
        "records": record_lookup
    }
    with open(outfile, 'w', encoding='utf-8') as json_file:
        json.dump(lookup, json_file, indent=2)

def get_record_lookup(infile: str, header_line: int = 2, start_line: int = 3, include_line_numbers: bool = DEFAULT_INCLUDE_LINE_NUMBERS) -> Dict[str, Any]:

    if not os.path.exists(infile):
        raise Exception(f"file '{infile}' does not exist")

    header_to_position_lookup = {}
    position_to_header_lookup = {}
    record_list = []
    record_ctr = 0

    with open(infile) as f:
        reader = csv.reader(f, delimiter='\t')
        for line_num, row in enumerate(reader):
            if line_num < header_line:
                logging.info(f"Will ignore line '{line_num}': {row}")
                continue
            if line_num == header_line:
                for field_ctr, field in enumerate(row):
                    header_to_position_lookup[field] = field_ctr
                    position_to_header_lookup[field_ctr] = field
                logging.info(f"Processed the header of tab-delimited file '{infile}'")
            elif line_num > header_line:
                record_lookup = {}

                if include_line_numbers:
                    record_lookup["line_num"] = line_num

                for field_ctr, value in enumerate(row):
                    field_name = position_to_header_lookup[field_ctr]
                    record_lookup[field_name] = value
                record_list.append(record_lookup)
                record_ctr += 1
        logging.info(f"Processed '{record_ctr}' records in csv file '{infile}'")

    return record_list


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
@click.option('--config_file', type=click.Path(exists=True), help=f"Optional: The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--header_line', help=f"Optional: The line number the header row begins - default is '{DEFAULT_HEADER_LINE}'")
@click.option('--include_line_numbers', is_flag=True, help=f"Optional: To include the line numbers in the JSON - default is '{DEFAULT_INCLUDE_LINE_NUMBERS}'")
@click.option('--infile', help="Required: The primary input file")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help="Optional: The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output final report file")
@click.option('--start_line', help=f"Optional: The line number the data rows begin - default is '{DEFAULT_START_LINE}'")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(config_file: str, header_line: int, include_line_numbers: bool, infile: str, logfile: str, outdir: str, outfile: str, start_line: int, verbose: bool):
    """Convert tab-delimited file into JSON file."""

    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)


    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        console.print(f"[yellow]--config_file was not specified and therefore was set to '{config_file}'[/]")

    if header_line is None:
        header_line = DEFAULT_HEADER_LINE
        console.print(f"[yellow]--header_line was not specified and therefore was set to '{header_line}'[/]")

    if include_line_numbers is None:
        include_line_numbers = DEFAULT_INCLUDE_LINE_NUMBERS
        console.print(f"[yellow]--include_line_numbers was not specified and therefore was set to '{include_line_numbers}'[/]")

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

    if outfile is None:
        outfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.json'
        )
        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")

    if start_line is None:
        start_line = DEFAULT_START_LINE
        console.print(f"[yellow]--start_line was not specified and therefore was set to '{start_line}'[/]")

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    check_infile_status(config_file, "yaml")

    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    convert_file(
        infile,
        outfile,
        start_line=start_line,
        header_line=header_line,
        include_line_numbers=include_line_numbers
    )

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()
