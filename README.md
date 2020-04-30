Process PDF files without using external tools, like web services or strange software that maybe stores your files somewhere, without caring for privacy.

The code of this tool is all here, and since it's a CLI it is really minimal and fast.

The library to deal with PDF files is [PyPDF2](https://pythonhosted.org/PyPDF2/), that is freely available as well.
For the future, a GUI is work in progress.

```
python pdf.py -h
usage: pdf.py [-h] [-d OUTPUTFILE] [--version] [-l [LOGFILE] | -ll [LOGFILE] |
              -lll [LOGFILE] | -llll [LOGFILE]]
              (-m file[page subset] [file[page subset] ...] | -e file[page subset] | -w FILE WATERMARKFILE)

Process PDF files

optional arguments:
  -h, --help            show this help message and exit
  -d OUTPUTFILE, --destination OUTPUTFILE
                        This is the path to processing output file;
  --version             show program's version number and exit
  -l [LOGFILE], --errorLog [LOGFILE]
                        Set log level to ERROR + optional log file path
  -ll [LOGFILE], --warningLog [LOGFILE]
                        Set log level to WARNING + optional log file path
  -lll [LOGFILE], --infoLog [LOGFILE]
                        Set log level to INFO + optional log file path
  -llll [LOGFILE], --debugLog [LOGFILE]
                        Set log level to DEBUG + optional log file path
  -m file[page subset] [file[page subset] ...], --merge file[page subset] [file[page subset] ...]
                        List of paths to pdf files to merge together (plus
                        additional page subset) in the provided order;
  -e file[page subset], --extract file[page subset]
                        Path to pdf file, and page subset, that have to be
                        extracted.
  -w FILE WATERMARKFILE, --watermark FILE WATERMARKFILE
                        Watermark your pdf file. A watermark file has to be
                        created before!
```


Usage example:
```
$ python pdf.py -d ./my_destination.pdf -m ./file1.pdf ./file2.pdf[6-15] ./file3.pdf[3,5-7]
```

will merge (-m) together file1.pdf with pages 6 to 15 of file2.pdf and pages 3 and 5 to 7 of file3.pdf
