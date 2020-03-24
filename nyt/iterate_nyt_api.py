#!/usr/bin/env python3
from nyt_api import NYTapi
from nyt_key import nyt_key
import datetime as dt
from handy_tools import daterange
"""
    This script iterates over a range of dates and save the results
    of the search as plain text to the file specified by the variable
    'filename_template'. 

    Note : You should probably create a directory and prefix it to 
        filename_template otherwise your working directory will
        be filled with data.

    In order to run this script you must create a file nyt_key.py with 
    your key set to the variable nyt_key as a string, i.e.:

    nyt_key.py :
        nyt_key = 'long_key_string_from_website'
"""
query = 'coronavirus'
start_date = dt.date(2019, 3, 13)
end_date = dt.date(2020, 3, 23)
filename_template = "nyt_data_{0}.txt"

#------------------------------------------------------------------------- 
preamble = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
search_base = "q={0}&fq={1}&page={2}&api-key={3}"
nyt_api = NYTapi( preamble, search_base, query, nyt_key )
for date in daterange( start_date, end_date ):
    nyt_api.set_date( date )
    with open(filename_template.format( date ), 'w') as f:
        f.write(nyt_api.url_pretty())
    for response_text in nyt_api.iterate_search_over_pages():
        with open(filename, 'a') as f:
            f.write( response_text )
#------------------------------------------------------------------------- 
