#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pickle

"""
    DEVELOPMENT SCRIPT.

    simple script to download the wiki page of the S&P 500 and extract 
    the table containing the S&P500 symbols and company information 
    (e.g. sector classification).

    Note that the parameter download_wiki exists as a development hack. 
    Set the parameter to True to download the page once. Set the parameter
    to false to 

    The output of the script is a pickle file that contains a Python list
    of dictionary elements. The dictionary maps each of the table headings
    to the table values for the corresponding company. It may be better to 
    have a look at the table given at the link:

    https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks

    So, for example, the first element in the list will be a dictionary with
    the following (key,value) pairs:
        ('Symbol', 'MMM'), ('Security', '3M Company'),  ... 

    This list-of-dictionaries will be saved to the file given by
    output_pickle_filename.
"""

def extract_cols_from_row( row, identifier='td') :
    cols = row.find_all(identifier)
    cols = [ele.text.strip() for ele in cols]
    return cols

download_wiki = False
output_pickle_filename = 'sp500_data.p'
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
raw_text_file = 'wiki_sp_500.raw'
response_text = ""

if download_wiki : 
    response = requests.get(url)
    response_text = response.text
    outfile = open( raw_text_file, 'w' )
    outfile.write( response_text )
    outfile.close()
else :
    infile = open( raw_text_file, 'r' )
    response_text = '\n'.join(infile.readlines())
    infile.close()

soup = BeautifulSoup(response_text, "html.parser")
table = soup.find('table')
table_body = table.find('tbody')
rows = table_body.find_all('tr')
labels = extract_cols_from_row( rows.pop(0), identifier='th' )
data = [dict(zip(labels, extract_cols_from_row( row ))) for row in rows]
pickle.dump(data, open(output_pickle_filename, 'wb'))
