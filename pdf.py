##
# @author Francesco Antoniazzi <francesco.antoniazzi1991@gmail.com>
 # @file Python script to easily deal with pdf files, without using web services or software you don't trust.
 # @desc Created on 2020-02-19 10:38:09 am
 #

import argparse
import logging
import re

from os.path import isfile, join, expanduser, realpath
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = None
pdf_writer = None

def file_path_subset_regex(file_path):
    m = re.match(r"^(.+)\[(.*)\]", file_path)
    if m is None:
        return file_path, []
    path = m.group(1)
    page_subset_string = m.group(2).replace(" ","").split(",")
    if page_subset_string[0] == "":
        return file_path, []
    page_list = []
    for subset_string in page_subset_string:
        mm = re.match(r"([1-9]\d*)(?:-([1-9]\d*))?", subset_string)
        if mm.group(2) is None:
            page_list.append(int(mm.group(1)))
        else:
            page_list += range(int(mm.group(1)), int(mm.group(2))+1)
    return path, page_list

def extract(file_path):
    global pdf_writer
    path, page_list = file_path_subset_regex(file_path)
    logging.debug(page_list)
    if not isfile(path):
        raise FileNotFoundError

    pdf_reader = PdfFileReader(path)
    pdf_page_number = pdf_reader.getNumPages()
    logging.warning("File has {} pages.".format(pdf_page_number))
    if page_list == []:
        logging.warning("Extracting the whole file {}".format(path))
        page_list = list(range(0,pdf_page_number))
    else:
        max_page_request = max(page_list)
        if pdf_page_number < max_page_request:
            logging.error("Wrong page selection from {}: requested page {} from file having {} pages.".format(path, max_page_request, pdf_page_number))
            raise ValueError

    for page in page_list:
        logging.warning("Extracting page {}".format(page))
        pdf_writer.addPage(pdf_reader.getPage(page))

def merge(file_path_list):
    for item in file_path_list:
        extract(item)
        

def main(args):
    global pdf_writer
    pdf_writer = PdfFileWriter()
    if not args["merge"] is None:
        merge(args["merge"])
    else:
        extract(args["extract"])

    logging.info("Writing output to {}".format(args["destination"]))
    with open(args["destination"], "wb") as output:
        pdf_writer.write(output)

if __name__ == "__main__":
    output_path = join(expanduser("~"), "Desktop", "output.pdf")
    parser = argparse.ArgumentParser(description="Process PDF files")

    parser.add_argument("-d", "--destination", default=output_path, help="This is the path to processing output file;")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--merge", nargs="+", help="List of paths to pdf files to merge together (plus additional page subset) in the provided order;")
    group.add_argument("-e", "--extract", help="Path to pdf file, and page subset, that have to be extracted.")

    main(vars(parser.parse_args()))