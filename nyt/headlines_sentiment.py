#!/usr/bin/env python3
#from textblob import TextBlob
#from textblob.sentiments import NaiveBayesAnalyzer
from handy_tools import daterange, mondays_in_interval
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict
import datetime as dt
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def iterate_headlines(headlines_file, n_max=10000) :
    for j, line in enumerate(headlines.readlines()):
        line = line.split(',')
        article_date, article_time = line.pop(-1).split('T')
        article_date = dt.datetime.strptime(article_date, '%Y-%m-%d').date()
        headline = ','.join(line)
        if j > n_max:
            break
        yield article_date, article_time.strip('\n'), headline

headlines = open( 'covid19_headlines_nyt.txt', 'r' )
sentiments = defaultdict(list)
start_date, end_date = None, None

for date, time, headline in iterate_headlines(headlines,n_max=5000) :
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(headline)
    sentiments[date].append( sentiment_dict['neg'] )
    end_date = date
    start_date = end_date if start_date is None else start_date

mondays = mondays_in_interval( start_date, end_date )
dates = [date for date in sentiments.keys()]
negativity = [np.max(sents) for sents in sentiments.values()] 

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot( dates, negativity, 'r', lw=2 )
for label in ax.get_xticklabels():
    label.set_rotation(40)
    label.set_horizontalalignment('right')
for day in mondays :
    ax.axvline( x=day, ymin=0, ymax=100 )
locator = mdates.AutoDateLocator(minticks=5, maxticks=9)
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
ax.set_xlim(start_date, end_date)
ax.set_ylabel('max negativity of daily NYT covid-19 press')
#ax.grid(True)
ax.set_title('negativity of NYT covid-19 coverage')
plt.tight_layout()
plt.show()
"""
for j, line in enumerate(headlines.readlines()) :
    line = line.split(',')
    article_date, article_time = line.pop(-1).split('T')
    article_date = dt.datetime.strptime(article_date, '%Y-%m-%d').date()
    headline = ','.join(line)
    blob = TextBlob(headline, analyzer=NaiveBayesAnalyzer())
    sentiments[article_date].append( blob.sentiment.p_neg )
    print(headline, '\n\t', blob.sentiment.p_neg)
    if j == 100:
        break
for date, article_sentiments in sentiments.items():
    article_sentiments = np.asarray(article_sentiments)
    print(date,np.mean(article_sentiments), 1./np.sqrt(len(article_sentiments)))
"""
