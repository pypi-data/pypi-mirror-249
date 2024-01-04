"""Compare two sorted review files line-by-line and column-by-column."""
import os
import sys
import click
import pathlib
import logging

import xlsxwriter

from typing import Dict, List
from datetime import datetime
from rich.console import Console


TUPLE_COLUMNS = [1,2,3,5]


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


def read_file(file_path, outdir):
    """Read a tab-delimited file and return its content as a list of lists."""
    logging.info(f"Going to read file '{file_path}'")
    with open(file_path, 'r', encoding="latin-1") as file:
        lines = file.readlines()
    header = lines[HEADER_LINE].strip().split('\t')
    header_index_to_name_lookup = {}
    header_name_to_index_lookup = {}
    filtered_header = []
    for i, h in enumerate(header, start=1):
        if i not in TUPLE_COLUMNS:
            logging.info(f"Ignore column number '{i}' with name")
            continue
        true_header_index = i - 1
        h = h.strip()
        header_index_to_name_lookup[true_header_index] = h
        header_name_to_index_lookup[h] = true_header_index
        filtered_header.append(h)

    data = []
    lookup = {}
    duplicate_lookup = {}
    duplicate_list = []
    duplicate_ctr = 0

    line_num = RECORDS_START_LINE
    for line in lines[RECORDS_START_LINE:]:
        fields = line.strip().split('\t')
        record = []
        for i, field in enumerate(fields, start=1):
            if i not in TUPLE_COLUMNS:
                continue
            true_header_index = i - 1
            field = field.strip()
            if true_header_index in header_index_to_name_lookup and header_index_to_name_lookup[true_header_index].lower() == "mutation":
                if field.endswith("()"):
                    field = field.rstrip("()").strip()

            record.append(field)
        line_num += 1
        rec_key = "::".join(record)
        if rec_key in lookup:
            duplicate_ctr += 1
            prev_line = lookup[rec_key]
            # duplicate_list.append([rec_key, f"{line_num}, {prev_line}"])
            if rec_key not in duplicate_lookup:
                duplicate_lookup[rec_key] = []
                duplicate_lookup[rec_key].append(f"{prev_line}")
            duplicate_lookup[rec_key].append(f"{line_num}")

            logging.error(f"Record '{rec_key}' encountered at line '{line_num}' and previous line '{prev_line}' in file '{file_path}' - so will not include this in the lookup")
            continue
            # raise Exception(f"Record '{rec_key}' encountered at line '{line_num}' and previous line '{prev_line}'")
        # data.append(record)
        lookup[rec_key] = line_num

    if duplicate_ctr > 0:
        outfile = os.path.join(outdir, f"duplicate_records_{os.path.basename(file_path)}.report.txt")
        generate_duplicates_report(
            filtered_header,
            f"Found '{duplicate_ctr}' duplicate records in file '{file_path}'",
            duplicate_lookup,
            outfile
        )
    else:
        logging.info(f"Did not encounter any duplicate records in file '{file_path}'")

    return filtered_header, header_index_to_name_lookup, header_name_to_index_lookup, lookup

    # return header, header_index_to_name_lookup, header_name_to_index_lookup, data

def get_ignore_columns_lookup(ignore_columns_str: str) -> Dict[str, bool]:
    ignore_columns_lookup = {}
    logging.info(f"Will ignore columns: {ignore_columns_str}")
    columns = ignore_columns_str.split(",")
    for column in columns:
        ignore_columns_lookup[column.strip()] = True
    return ignore_columns_lookup


def analyze_files(
        file1_path: str,
        file2_path: str,
        outdir: str,
    ):
    """Compare two tab-delimited files and store differences."""

    header1, header_index_to_name_lookup1, header_name_to_index_lookup1, lookup1 = read_file(file1_path, outdir)
    header2, header_index_to_name_lookup2, header_name_to_index_lookup2, lookup2 = read_file(file2_path, outdir)

    # if header1 != header2:
    #     print("Headers of the two files are different.")
    #     return

    logging.info(f"Going to compare contents of the two files now")

    missing_in_file2_ctr = 0
    missing_in_file2_list = []
    found_in_file2_ctr = 0

    for k1, line1 in lookup1.items():

        if k1 not in lookup2:
            logging.error(f"Did not find record '{k1}' (at line '{line1}' in file1) in file2")
            missing_in_file2_ctr += 1
            missing_in_file2_list.append([k1, line1])
        else:
            found_in_file2_ctr += 1



    missing_in_file1_ctr = 0
    missing_in_file1_list = []
    found_in_file1_ctr = 0

    for k2, line2 in lookup2.items():

        if k2 not in lookup1:
            logging.error(f"Did not find record '{k2}' (at line '{line2}' in file2) in file2")
            missing_in_file1_ctr += 1
            missing_in_file1_list.append([k2, line2])
        else:
            found_in_file1_ctr += 1


    if missing_in_file1_ctr > 0:
        print(f"Could not find '{missing_in_file1_ctr}' records in file 1 that were in file 2")
        print("See the log file for details")
        outfile = os.path.join(outdir, "records_missing_from_file_1.txt")
        generate_missing_records_report(
            outfile,
            missing_in_file1_ctr,
            missing_in_file1_list,
            file1_path,
            file2_path,
            f"The following '{missing_in_file1_ctr}' records were not found in file 1 '{file1_path}'",
            header1
        )
    else:
        print(f"Found all '{found_in_file1_ctr}' records in file 1 that were in file 2")

    if missing_in_file2_ctr > 0:
        print(f"Could not find '{missing_in_file2_ctr}' records in file 2 that were in file 1")
        print("See the log file for details")
        outfile = os.path.join(outdir, "records_missing_from_file_2.txt")
        generate_missing_records_report(
            outfile,
            missing_in_file2_ctr,
            missing_in_file2_list,
            file1_path,
            file2_path,
            f"The following '{missing_in_file2_ctr}' records were not found in file 2 '{file2_path}'",
            header1
        )
    else:
        print(f"Found all '{found_in_file2_ctr}' records in file 2 that were in file 1")



def generate_missing_records_report(outfile, missing_record_ctr, missing_record_list, file1_path, file2_path, msg, header):

    with open(outfile, 'w') as of:
        of.write(f"## sorted review file 1: {file1_path}\n")
        of.write(f"## sorted review file 2: {file2_path}\n")
        of.write(f"## {msg}\n")
        of.write("\t".join(header) + "\tLine Number\n")
        for missing_list in missing_record_list:
            missing_record = missing_list[0]
            line_num = missing_list[1]
            rec = missing_record.replace("::", "\t")
            of.write(f"{rec}\t{line_num}\n")


    logging.info(f"Wrote missing records report file '{outfile}'")
    print(f"Wrote missing records report file '{outfile}'")


def generate_duplicates_report(
    header: List[str],
    msg: str,
    duplicate_lookup: Dict[str, List[str]],
    # duplicate_list: List[List[str]],
    outfile: str
    ) -> None:

    with open(outfile, 'w') as of:
        of.write(f"## {msg}\n")
        of.write("\t".join(header) + "\tLine Number\n")
        for record, line_num_list in duplicate_lookup.items():
            rec = record.replace("::", "\t")
            lines = ", ".join(line_num_list)
            of.write(f"{rec}\t{lines}\n")

        # for parts in duplicate_list:
        #     record = parts[0]
        #     line_num = parts[1]
        #     rec = record.replace("::", "\t")
        #     of.write(f"{rec}\t{line_num}\n")

    logging.info(f"Wrote duplicate records report file '{outfile}'")
    print(f"Wrote duplicate records report file '{outfile}'")


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



@click.command()
@click.option('--logfile', help="Optional: The log file")
@click.option('--outdir', help="Optional: The output directory where logfile and default output file will be written - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output file to which differences will be written to - default is '{DEFAULT_OUTFILE}'")
@click.option('--sorted_review_file_1', help="Required: The first sorted review file (.tsv)")
@click.option('--sorted_review_file_2', help="Required: The second sorted review file (.tsv)")
@click.option('--verbose', is_flag=True, help=f"Optional: Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(logfile: str, outdir: str, outfile: str, sorted_review_file_1: str, sorted_review_file_2: str, verbose: bool):
    """Compare two sorted review files line-by-line and column-by-column."""

    error_ctr = 0

    if sorted_review_file_1 is None:
        error_console.print("--sorted_review_file_1 was not specified")
        error_ctr += 1

    if sorted_review_file_2 is None:
        error_console.print("--sorted_review_file_2 was not specified")
        error_ctr += 1

    if error_ctr > 0:
        error_console.print("Required command-line arguments were not provided")
        sys.exit(1)

    check_infile_status(sorted_review_file_1)
    check_infile_status(sorted_review_file_2)

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


    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )


    analyze_files(sorted_review_file_1, sorted_review_file_2, outdir)


    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()
