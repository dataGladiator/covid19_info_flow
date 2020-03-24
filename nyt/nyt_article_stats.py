#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pickle

article_listdict_name = 'nyt_articles_dict.p'
article_listdict = pickle.load( open(article_listdict_name, 'rb') )

for article in article_listdict:
    print( article['headline'] )
print( len(article_listdict) )
