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
        
def watermark(args):
    global pdf_writer
    from reportlab.pdfgen import canvas
    
    if isfile(args[0]):
        path = args[0]
        watermark = args[1]
    else:
        logging.warning("First argument is not a path to file: will use it as watermark")
        if not isfile(args[1]):
            logging.error("Second argument should then be a path to file. Aborting")
            raise FileNotFoundError
        else:
            path = args[1]
            watermark = args[0]
    logging.warning("Path to file: {}; watermark: {}".format(path,watermark))
    c = canvas.Canvas("watermark.pdf")
    c.setFontSize(22)
    c.setFont('Helvetica-Bold', 36)
    c.drawString(15, 15, watermark)
    c.save()
    
    #with open("watermark.pdf", "rb") as waterfile:
    watermark_object = PdfFileReader("watermark.pdf")
        
    pdf_reader = PdfFileReader(path)
    page_count = pdf_reader.getNumPages()
    for page_number in range(page_count):
        input_page = pdf_reader.getPage(page_number)
        input_page.mergePage(watermark_object.getPage(0))
        pdf_writer.addPage(input_page)

def main(args):
    global pdf_writer
    pdf_writer = PdfFileWriter()
    if not args["merge"] is None:
        merge(args["merge"])
    elif not args["extract"] is None:
        extract(args["extract"])
    else:
        watermark(args["watermark"])

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
    group.add_argument("-w", "--watermark", nargs=2, help="Watermark your pdf file.")

    main(vars(parser.parse_args()))
