#!/bin/python3
# 
# This is an easy Python3 tool to manage pdf files.
# Sometimes, when you install these kind of software, you give the right
# to the software to use your file as they want, send it to the internet,
# which is a huge lack of privacy that we accept, since we don't know.
# 
# This software comes with several setups, one of which is fully included
# in this file. You can easily manage your pdfs with just a command line, 
# and by having a short look to this file, you'll see that we're actually
# importing two external libraries: PyPDF2 (BSD) and reportlab (BSD), which are open source and available
# for check, and that is a project that is totally independent from this one.
#
#
# Copyright (C) 2020 Francesco Antoniazzi <francesco.antoniazzi1991@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import logging
import re
from sys import stderr, exit

from os.path import isfile, join, expanduser, realpath
from PyPDF2 import PdfFileReader, PdfFileWriter

parser = None
pdf_writer = None

def file_path_subset_regex(file_path):
    # This function uses regex to analyze the input of the command line
    # and decide how to treat each file, and each subset of pages
    m = re.match(r"^(.+)\[(.*)\]", file_path)
    if m is None:
        # this is the case when you give just the name of the file, without
        # a page subset
        return file_path, []
    
    path = m.group(1)
    page_subset_string = m.group(2).replace(" ","").split(",")
    if page_subset_string[0] == "":
        # this is the case in which you give a file like ./myfile.pdf[]
        # still there is no page subset
        return file_path, []
    page_list = []
    for subset_string in page_subset_string:
        mm = re.match(r"([1-9]\d*)(?:-([1-9]\d*))?", subset_string)
        if mm is None:
            # this happens when you use 0 as first page
            logging.error("Subset page format is wrong: it should be given as [page,pageStart-pageEnd] where the first page of the pdf file is page 1")
        if mm.group(2) is None:
            page_list.append(int(mm.group(1)))
        else:
            page_list += range(int(mm.group(1)), int(mm.group(2))+1)
        logging.debug("Page list: {}".format(page_list))
    return path, page_list

def extract(file_path):
    global pdf_writer
    path, page_list = file_path_subset_regex(file_path)
    if not isfile(path):
        logging.error("{} not found".format(file_path))
        return False

    pdf_reader = PdfFileReader(path)
    pdf_page_number = pdf_reader.getNumPages()
    logging.debug("File {} has {} pages.".format(path, pdf_page_number))
    if page_list == []:
        logging.warning("Extracting the whole file {}".format(path))
        page_list = list(range(1,pdf_page_number+1))
    else:
        max_page_request = max(page_list)
        if pdf_page_number < max_page_request:
            logging.error("Wrong page selection from {}: requested page {} from file having {} pages.".format(path, max_page_request, pdf_page_number))
            return False

    for page in page_list:
        logging.info("Extracting page {}".format(page))
        pdf_writer.addPage(pdf_reader.getPage(page-1))
    return True

def merge(file_path_list):
    for item in file_path_list:
        logging.info("Merging file {}".format(item))
        extract(item)
        
def watermark(args):
    global pdf_writer
    
    if isfile(args[0]) and isfile(args[1]):
        path = args[0]
        watermark = args[1]
        logging.warning("Path to pdf file: {}".format(path))
        logging.warning("Path to pdf watermark: {}".format(watermark))
    else:
        return False
        
    pdf_reader = PdfFileReader(path)
    watermark_reader = PdfFileReader(watermark)
    
    for page_number in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_number)
        page.mergePage(watermark_reader.getPage(0))
        pdf_writer.addPage(page)
    return True
        
def setup_logging(args):
    # This function interprets the arguments and defines a configuration
    # for the logging functionality
    FORMAT = "%(asctime)-15s %(filename)s[%(funcName)s] %(levelname)s:%(message)s"
    ldict = {"errorLog": logging.ERROR, "warningLog": logging.WARNING, "infoLog": logging.INFO, "debugLog": logging.DEBUG}
    for k,v in ldict.items():
        if k in args:
            if args[k]:
                logging.basicConfig(filename=args[l], level=v,format=FORMAT)
                logging.debug("Setup logging with level {} towards {}".format(k,args[k]))
            else:
                logging.basicConfig(stream=stderr, level=v,format=FORMAT)
                logging.debug("Setup logging with level {} towards stderr".format(k))
            return
    logging.basicConfig(format=FORMAT)

def main(args):
    global pdf_writer
    
    setup_logging(args)
    logging.debug(args)
    
    pdf_writer = PdfFileWriter()
    result = False
    if "merge" in args:
        logging.info("Merge files procedure starts")
        result = merge(args["merge"])
    elif "extract" in args:
        logging.info("Extract pages procedure starts")
        result = extract(args["extract"])
    else:
        logging.info("PDF watermarking procedure starts")
        result = watermark(args["watermark"])

    if result:
        logging.info("Writing output to {}".format(args["destination"]))
        with open(args["destination"], "wb") as output:
            pdf_writer.write(output)
    return result

if __name__ == "__main__":
    output_path = join(expanduser("~"), "Desktop", "output.pdf")
    parser = argparse.ArgumentParser(description="Process PDF files")

    parser.add_argument("-d", "--destination", default=output_path, 
    metavar=("OUTPUTFILE"), help="This is the path to processing output file;")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    
    logGroup = parser.add_mutually_exclusive_group()
    logGroup.add_argument("-l", "--errorLog", nargs="?", default=argparse.SUPPRESS,
        metavar=("LOGFILE"), help="Set log level to ERROR + optional log file path")
    logGroup.add_argument("-ll", "--warningLog", nargs="?", default=argparse.SUPPRESS,
        metavar=("LOGFILE"), help="Set log level to WARNING + optional log file path")
    logGroup.add_argument("-lll", "--infoLog", nargs="?", default=argparse.SUPPRESS,
        metavar=("LOGFILE"), help="Set log level to INFO + optional log file path")
    logGroup.add_argument("-llll", "--debugLog", nargs="?", default=argparse.SUPPRESS,
        metavar=("LOGFILE"), help="Set log level to DEBUG + optional log file path")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--merge", nargs="+", default=argparse.SUPPRESS, 
        metavar=("file[page subset]"), help="List of paths to pdf files to merge together (plus additional page subset) in the provided order;")
    group.add_argument("-e", "--extract", default=argparse.SUPPRESS, 
        metavar=("file[page subset]"), help="Path to pdf file, and page subset, that have to be extracted.")
    group.add_argument("-w", "--watermark", nargs=2, default=argparse.SUPPRESS, 
        metavar=("FILE", "WATERMARKFILE"), help="Watermark your pdf file. A watermark file has to be created before!")

    exit(main(vars(parser.parse_args())))
