Process PDF files without using external tools, like web services or strange software that maybe stores your files somewhere, without caring for privacy.

The code of this tool is all here, and since it's a CLI it is really minimal and fast.

The library to deal with PDF files is PyPDF2, that is freely available as well.
For the future, a GUI is work in progress.

```
usage: pdf.py [-h] [-d DESTINATION] (-m MERGE [MERGE ...] | -e EXTRACT)

optional arguments:
  -h, --help            show this help message and exit
  -d DESTINATION, --destination DESTINATION
                        This is the path to processing output file;
  -m MERGE [MERGE ...], --merge MERGE [MERGE ...]
                        List of paths to pdf files to merge together (plus additional page subset) in the provided order;
  -e EXTRACT, --extract EXTRACT
                        Path to pdf file, and page subset, that have to be extracted.
```