#!/usr/bin/python
 
import sys
import os.path
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *

## functions

def customizations(record):
    """applies some smart customizations to the raw BibTex input.
    Taken from: https://bibtexparser.readthedocs.io/en/v0.6.2/tutorial.html#customizations
    
    Use some functions delivered by the library
    :param record: a record
    :returns: -- customized record
    """
    record = type(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    return record

## execution

if len(sys.argv) < 2:
    print "bibtex-parser.py"
    print "USAGE:\t./bibtex-parser.py <library-file> <mode>"
    print "\033[91m#TODO: implement <mode>\033[0m"
    exit(1)

bibfilename = sys.argv[1]

if not os.path.isfile(bibfilename):
    print "bibtex-parser.py: \033[91mthis is not a file!\033[0m"
    exit(2)

with open(bibfilename) as bibtex_file:
    #bib_database = bibtexparser.load(bibtex_file)
    parser = BibTexParser()
    parser.customization = customizations
    bib_database = bibtexparser.load(bibtex_file, parser=parser)
    
    for element in bib_database.entries:
        print element
        


