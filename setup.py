#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  setup.py
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

from setuptools import setup, find_packages

setup(
    name="PdfExtract",
    version="1.0",
    packages=find_packages(),
    scripts=["pdf.py"],

    install_requires=["pypdf2>=1.26.0"],


    # metadata to display on PyPI
    author="Francesco Antoniazzi",
    author_email="francesco.antoniazzi1991@gmail.com",
    description="PdfExtract package",
    keywords="pdf extract merge watermark",
    url="https://github.com/fr4ncidir/PDFextract",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/fr4ncidir/PDFextract/issues",
        "Documentation": "https://github.com/fr4ncidir/PDFextract/blob/master/README.md",
        "Source Code": "https://github.com/fr4ncidir/PDFextract",
    },
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable"
    ]
)
