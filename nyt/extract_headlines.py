#!/usr/bin/env python3
from handy_tools import daterange, dt
import json
import pickle

"""
    This script converts the raw json response of the NYT api into a 
    list of dictionaries. Each list corresponds to a news article and
    the corresponding dictionary element provides the following keys:

info_keys = ['abstract', 'web_url', 'snippet', 'lead_paragraph', \
             'print_section', 'print_page', 'source', 'headline', \
             'keywords', 'pub_date', 'document_type', 'news_desk',\
             'section_name', 'type_of_material', 'word_count']

    In some cases, the value associated with the key is None - in that
    case, the API

    at the first level, the reponse is:
     status - should be 'OK'
     copyright - standard thing
     reponse - the data we want. Another json dictionary

    response contains two keys : docs and meta. 
    meta contains three keys : hits, offset and time.
    hits is of interest b/c it tells us how many pages there will be

    docs returns a list of dictionaries. Each element in the list
    corresponds to a hit.

    a docs_item (i.e. element of the docs list) contains the following
    keys:
        abstract
        web_url
        snippet
        lead_paragraph
        print_section
        print_page
        source
        multimedia
        headline
        keywords
        pub_date
        document_type
        news_desk
        section_name
        byline
        type_of_material
        _id
        word_count
        uri
"""

info_keys = ['abstract', 'web_url', 'snippet', 'lead_paragraph', \
             'print_section', 'print_page', 'source', 'headline', \
             'keywords', 'pub_date', 'document_type', 'news_desk',\
             'section_name', 'type_of_material', 'word_count']

def parse_doc_item(doc, item):
    value = None
    try :
        value = doc[item]
    except KeyError :
        value = None
    if item == 'headline':
        value = value['main']
    elif item == 'keywords':
        value = [ u['value'] for u in value]

    return value

def parse_doc(doc) :
    dict_as_list = []
    for item in info_keys:
        dict_as_list.append( (item, parse_doc_item(doc, item)) )
    return dict(dict_as_list)

start_date = dt.date(2019, 11, 1)
end_date = dt.date(2020, 3, 13)
filename_template = "nyt_data/nyt_data_{0}.txt"
to_ignore = ['multimedia','byline','_id', 'uri', 'headline', 'keywords']
articles = []

for j, date in enumerate( daterange( start_date, end_date )) :
    data = open( filename_template.format( date ), 'r' ).readlines()
    if len(data) > 1:
        raw_response = json.loads( data[2] )
        status = raw_response['status']
        response = raw_response['response']
        docs = response['docs']
        for doc in docs:
            articles.append( parse_doc( doc ) )

pickle.dump(articles, open( 'nyt_articles_dict.p', 'wb'))
