#!/usr/bin/python
 
import sys
import os.path
import argparse
import string
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



parser = argparse.ArgumentParser(description='Read a BibTeX file and create a TeX summary (optionally based on keywords).')
parser.add_argument('bibfilename', metavar='bibfile', type=str, nargs=1,
                    help='a BibTeX file to be summarized')
parser.add_argument('outputfilename', metavar='outfile', type=str, nargs=1,
                    help='an output file name')
parser.add_argument('--must_contain', nargs='+', type=str,
                    help='optional search terms (all have to match)')
parser.add_argument('--may_contain', nargs='+', type=str,
                    help='optional search terms (any matches)')

args = parser.parse_args()

bibfilename = args.bibfilename
outputfilename = args.outputfilename
keywords_req = args.must_contain
keywords_opt = args.may_contain

print(keywords_req)
print(keywords_opt)
exit(0)

if not os.path.isfile(bibfilename):
    print "bibtex-summarizer.py: \033[91mthis is not a file!\033[0m"
    exit(2)

if os.path.isfile(outputfilename):
    print "bibtex-summarizer.py: \033[91moutput file already exists!\033[0m"
    exit(2)

output = u''

with open(bibfilename) as bibtex_file:
    #bib_database = bibtexparser.load(bibtex_file)
    parser = BibTexParser()
    parser.customization = customizations
    bib_database = bibtexparser.load(bibtex_file, parser=parser)
    
    for element in bib_database.entries:
        if element.has_key('ID'):
            citeid = element['ID'] if element.has_key('ID') else "<NO ID>"
            title = element['title'] if element.has_key('title') else "<NO TITLE>"
            author = element['author'] if element.has_key('author') else ("<NO AUTHOR>",)
            abstract = element['abstract'] if element.has_key('abstract') else "<NO ABSTRACT>"
            
            output += u'\\cite{{{}}}: \\\\\n'.format(citeid)
            output += u'\t\\begin{displayquote}\n'
            output += u'\t\t\\textbf{{{0}}} \n\t\tby \\textit{{{1}}}: \\\\\n\t\t{2}\n'.format(title, ', '.join(author), abstract)
            output += u'\t\\end{displayquote}\n\n'
            #for author in element['author']:
            #    print author
        

print output
with open(outputfilename, "wb") as f:
   f.write(output.encode("UTF-8"))

