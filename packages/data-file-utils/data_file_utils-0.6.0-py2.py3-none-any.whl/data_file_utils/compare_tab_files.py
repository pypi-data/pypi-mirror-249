"""Compare two sorted review files line-by-line and column-by-column."""
import os
import sys
import click
import pathlib
import logging
import pathlib

import xlsxwriter

from typing import Dict, Optional
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler


DEFAULT_IGNORE_COLUMNS = False


HEADER_LINE = 1
RECORDS_START_LINE = 2
MAX_COLUMN_COUNT = 0

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_OUTFILE = os.path.join(
    DEFAULT_OUTDIR,
    os.path.splitext(os.path.basename(__file__))[0] + '.diff.txt'
)


DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'conf',
    'config.json'
)

DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()


def get_column_number_to_column_letters_lookup(max_column_number: int = MAX_COLUMN_COUNT) -> Dict[int, str]:
    column_numbers = [x for x in range(max_column_number)]
    lookup = {}
    for column_number in column_numbers:
        column_letter = xlsxwriter.utility.xl_col_to_name(column_number)
        column_number += 1
        logging.debug(f"Converted column number '{column_number}' to column letter '{column_letter}'")
        lookup[column_number] = column_letter
    return lookup


def read_file(file_path):
    """Read a tab-delimited file and return its content as a list of lists."""
    logging.info(f"Going to read file '{file_path}'")
    with open(file_path, 'r', encoding="latin-1") as file:
        lines = file.readlines()
    header = lines[HEADER_LINE].strip().split('\t')
    header_index_to_name_lookup = {}
    header_name_to_index_lookup = {}
    for i, h in enumerate(header):
        header_index_to_name_lookup[i] = h
        header_name_to_index_lookup[h] = i
    data = [line.strip().split('\t') for line in lines[RECORDS_START_LINE:]]
    return header, header_index_to_name_lookup, header_name_to_index_lookup, data

def get_ignore_columns_lookup(ignore_columns_str: str) -> Dict[str, bool]:
    ignore_columns_lookup = {}
    logging.info(f"Will ignore columns: {ignore_columns_str}")
    columns = ignore_columns_str.split(",")
    for column in columns:
        ignore_columns_lookup[column.strip()] = True
    return ignore_columns_lookup


def compare_files(file1_path, file2_path, ignore_columns: bool, ignore_columns_str: Optional[str]):
    """Compare two tab-delimited files and store differences."""
    header1, header_index_to_name_lookup1, header_name_to_index_lookup1, data1 = read_file(file1_path)
    header2, header_index_to_name_lookup2, header_name_to_index_lookup2, data2 = read_file(file2_path)

    if ignore_columns:
        ignore_columns_lookup = get_ignore_columns_lookup(ignore_columns_str)

    # if header1 != header2:
    #     print("Headers of the two files are different.")
    #     return

    logging.info(f"Going to compare contents of the two files now")

    max_rows = max(len(data1), len(data2))
    differences = []
    max_max_columns = 0

    for i in range(1, max_rows + 1):
        if i <= len(data1):
            row1 = data1[i - 1]
        else:
            row1 = [""] * len(header1)

        if i <= len(data2):
            row2 = data2[i - 1]
        else:
            row2 = [""] * len(header2)

        max_columns = max(len(row1), len(row2))
        if max_columns > max_max_columns:
            max_max_columns = max_columns

        # max_columns = 59

        for j in range(0, max_columns):

            cell1 = row1[j] if j < len(row1) else ""
            cell2 = row2[j] if j < len(row2) else ""

            if cell1 != cell2:
                if ignore_columns and j in header_index_to_name_lookup1 and header_index_to_name_lookup1[j] in ignore_columns_lookup:
                    logging.info(f"Found differences in cell 1 '{cell1}' and cell 2 '{cell2}' but will ignore")
                    continue
                # logging.info(f"i '{i}' j '{j}' max_columns '{max_columns}' max_rows '{max_rows}' cell1 '{cell1}' cell2 '{cell2}'")
                differences.append((i, header1[j] if j < len(header1) else header2[j], j + 1, cell1, cell2))

    global MAX_COLUMN_COUNT
    MAX_COLUMN_COUNT = max_max_columns
    return differences


def compare_files_v1(file1_path, file2_path):
    """Compare two tab-delimited files and store differences."""
    header1, data1 = read_file(file1_path)
    header2, data2 = read_file(file2_path)

    logging.info(f"Going to compare contents of the two files now")
    # if header1 != header2:
    #     print("Headers of the two files are different.")
    #     return

    # differences = []

    # for i, (row1, row2) in enumerate(zip(data1, data2), start=2):
    #     for j, (cell1, cell2) in enumerate(zip(row1, row2), start=1):
    #         if cell1 != cell2:
    #             differences.append((i, header1[j-1], j, cell1, cell2))

    max_rows = max(len(data1), len(data2))
    differences = []

    for i in range(1, max_rows + 1):
        if i <= len(data1):
            row1 = data1[i - 1]
        else:
            row1 = [""] * len(header1)

        if i <= len(data2):
            row2 = data2[i - 1]
        else:
            row2 = [""] * len(header2)

        for j, (cell1, cell2) in enumerate(zip(row1, row2), start=1):
            if cell1 != cell2:
                differences.append((i, header1[j - 1], j, cell1, cell2))

    return differences



def check_infile_status(infile: str = None, extension: str = None) -> bool:


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


def setup_filehandler_logger(logfile: str = None):

    # Create handlers
    # c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=logfile)

    # c_handler.setLevel(DEFAULT_LOGGING_LEVEL)
    f_handler.setLevel(DEFAULT_LOGGING_LEVEL)

    # Create formatters and add it to handlers
    f_format = logging.Formatter(DEFAULT_LOGGING_FORMAT)
    # c_format = logging.Formatter("%(levelname)-7s : %(asctime)s : %(message)s")

    # c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    # logging.addHandler(c_handler)
    logging.addHandler(f_handler)


@click.command()
@click.option('--ignore_columns', is_flag=True, help=f"Optional: Ignore columns specified in --ignore_columns_str - default is '{DEFAULT_IGNORE_COLUMNS}'")
@click.option('--ignore_columns_str', help=f"Optional: comma-separated list of column headers wrapped in quotes")
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help="Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output file to which differences will be written to - default is '{DEFAULT_OUTFILE}'")
@click.option('--tab_file_1', help="Required: The first sorted review file (.tsv)")
@click.option('--tab_file_2', help="Required: The second sorted review file (.tsv)")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(ignore_columns: bool, ignore_columns_str: str, logfile: str, outdir: str, outfile: str, tab_file_1: str, tab_file_2: str, verbose: bool):
    """Compare two sorted review files line-by-line and column-by-column."""

    error_ctr = 0

    if tab_file_1 is None:
        error_console.print("--tab_file_1 was not specified")
        error_ctr += 1

    if tab_file_2 is None:
        error_console.print("--tab_file_2 was not specified")
        error_ctr += 1

    if error_ctr > 0:
        error_console.print("Required command-line arguments were not provided")
        sys.exit(1)

    check_infile_status(tab_file_1)
    check_infile_status(tab_file_2)

    if ignore_columns is None:
        ignore_columns = DEFAULT_IGNORE_COLUMNS
        console.print(f"[yellow]--ignore_columns was not specified and therefore was set to '{ignore_columns}'[/]")


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
        outfile = DEFAULT_OUTFILE
        console.print(f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]")

    if ignore_columns:
        if ignore_columns_str is None:
            console.print(f"[bold red]--ignore_columns was specified but --ignore_columns_str was not specified[/]")
            sys.exit(-1)

    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    differences = compare_files(
        tab_file_1,
        tab_file_2,
        ignore_columns,
        ignore_columns_str
    )

    if differences:
        print(f"[bold red]{len(differences)} differences found[/]")
        logging.info(f"{len(differences)} differences found")

        lookup = get_column_number_to_column_letters_lookup(MAX_COLUMN_COUNT)

        with open(outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## tab-delimited file 1: {tab_file_1}\n")
            of.write(f"## tab-delimited file 2: {tab_file_2}\n")
            of.write(f"## logfile: {logfile}\n")

            of.write("Line #\tColumn Name\tColumn #\tColumn Letter\tValue in File 1\tValue in File 2\n")
            for diff in differences:
                excel_column_letters = lookup[diff[2]]
                of.write(f"{diff[0]}\t{diff[1]}\t{diff[2]}\t{excel_column_letters}\t{diff[3]}\t{diff[4]}\n")

        logging.info(f"Wrote differences to output file '{outfile}'")
        if verbose:
            print(f"Wrote differences to output file '{outfile}'")

    else:
        print("[green]No differences found.[/]")
        logging.info("No differences found.")

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()
