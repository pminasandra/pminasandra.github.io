#/usr/bin/env python3
"""
Replaces citations of the form %%fullcite:citeentry%% with the appropriate citation entry
from a provided bibfile.
"""

import os
import os.path
import re

import bibtexparser

## CONFIG
SPECIAL_PMIN = True
SPECIAL_AUTHOR_NAME = "Minasandra, Pranav"
SPECIAL_AUTHOR_HTML="""<span class="special-author">%%name%%</span>"""
MAX_AUTHORS = 4

CITATION_HTML = """<div class="citation">
<span class="author">%%authorlist%%</span>
<span class="title">%%title%%</span>
<span class="journal">%%journal%%</span>
<span class="number">%%number%%</span>
<span class="pages">%%pages%%</span>
<span class="year">(%%year%%)</span>
<span class="doi">DOI:<a href="%%doiurl%%" target="_blank">%%doi%%</a></span>
</div>"""

bibentries = open('Resources/mypapers.bib').read()
MYPAPERS = bibtexparser.bparser.parse(bibentries).entries
MYPAPERS = {entry['ID']: entry for entry in MYPAPERS}

def pretty_author_name(name):
    lastname = name.split(',')[0]
    remaining_names = name.split(',')[1]
    initials = [n[0] for n in remaining_names.split()]

    return ''.join(initials) + '&nbsp;' + lastname

def pretty_author_names(authorlist):
    num_auth = len(authorlist)
    authtext = ""

    if len(authorlist) == 1:
        return authorlist[0]

    if num_auth <= MAX_AUTHORS:
        for name in authorlist[:-1]:
            authtext += name
            if num_auth > 2:
                authtext += ", "
            else:
                authtext += " "

        authtext += 'and ' + authorlist[-1]
        return authtext

    else:
        CUT_ID = num_auth - MAX_AUTHORS
        for name in authorlist[:-CUT_ID]:
            authtext += name
            authtext += ", "

        authtext += '<em>et&nbsp;al</em>'
        return authtext


def pretty_author_list(authors):
    authorlist = authors.split(' and ')
    newlist = []

    for name in authorlist:
        newname = pretty_author_name(name)
        if SPECIAL_PMIN:
            if name == SPECIAL_AUTHOR_NAME:
                newname = SPECIAL_AUTHOR_HTML.replace('%%name%%', newname)
        newlist.append(newname)

    return pretty_author_names(newlist)



def pretty_doi(doi):
    if doi.startswith('https://') or doi.startswith('http://'):
        doilist = doi.split('/')
        doinew = '/'.join(doilist[3:]) #get rid of https:// and domain
        return doinew

    return doi

def pretty_doiurl(doi):
    if doi.startswith('https://') or doi.startswith('http://'):
        return doi
    else:
        return 'https://doi.org/' + doi

def process_bibentry(bibentry):
    html = CITATION_HTML[:]
    targets = {
        '%%title%%': 'title',
        '%%authorlist%%': 'author',
        '%%journal%%': 'journal',
        '%%number%%': 'number',
        '%%pages%%': 'pages',
        '%%year%%': 'year',
        '%%doi%%': 'doi',
        '%%doiurl%%': 'doi'
    }

    for target in targets:
        if targets[target] in bibentry:
            if targets[target] not in ['author', 'doi', 'doiurl']:
                html = html.replace(target, bibentry[targets[target]])
            else:
                if targets[target] == 'author':
                    html = html.replace(target, pretty_author_list(bibentry[targets[target]]))
                elif target == '%%doi%%':
                    html = html.replace(target, pretty_doi(bibentry[targets[target]]))
                elif target == '%%doiurl%%':
                    html = html.replace(target, pretty_doiurl(bibentry[targets[target]]))
        else:
            html = html.replace(target, '')

    html.replace('--', '–')
    return html


def extract_citations(html_text):
    # Regular expression pattern to match %%cite:variable%% and capture the variable
    pattern = r'%%cite:(.*?)%%'
    
    # Find all matches in the HTML text
    citations = re.findall(pattern, html_text)
    
    return citations


def replace_citations(html_text, citations, filename):
    for citation in citations:
        print(f'In {filename}, adding citation for {citation}.')
        bibentry = MYPAPERS[citation]
        bibtext = process_bibentry(bibentry)
        bibtext = f'<!--begincite:{citation}--!>\n' + bibtext + f'\n<!--endcite:{citation}--!>\n'

        html_text = html_text.replace('%%cite:'+citation+'%%', bibtext)


    return html_text


def recursive_add_citations(dirname="."):
    os.chdir(dirname)
    current_dir = os.getcwd()
    available_htmls = [f for f in os.listdir() if f.endswith('.html')]
    for htmlfile in available_htmls:
        with open(htmlfile) as htf:
            htcontent = htf.read()
            citations = extract_citations(htcontent)

        if len(citations) == 0:
            continue

        print(f"Found citations in {current_dir}/{htmlfile}")
        htcontent = replace_citations(htcontent, citations, htmlfile)
        with open(htmlfile, 'w') as htf:
            htf.write(htcontent)

    available_dirs = [f for f in os.listdir() if os.path.isdir(f)]
    for dir_ in available_dirs:
        print(f"Processing directory: {dir_}")
        recursive_add_citations(dirname=os.path.join(current_dir, dir_))


if __name__ == "__main__":
    recursive_add_citations()