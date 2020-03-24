import requests
import json
import time

class NYTapi :
    """
    A class used to iterate queries to the NYT api over all avaible pages. 

    Attributes
    ----------
    preamble : str
        the url string that forms the prefix to the query url.
    search_base : str
        the unformatted string that forms the base of the query suffix.
    query : str
        the search term to be provided to the NYT. 
    key : str
        the user key provide by the NYT api.
    page : int
        the results page to be querried.
    hits_per_page : int
        a fixed paramter of the NYT api (10).
    fq : str, optional
        a search refinement paramter, here used to restrict the search date. 
    max_pages : int, optional
        a parameter to restrict the number of results to be iterated through.

    Methods
    -------
    url : str
        formats the complete search url according to current parameters.
    url_pretty : str
        same as self.url but with nicer formatting.
    search : requests.Response 
        submits self.url() to the web and returns response. 
    compute_n_pages : int
        computes the number of pages in the NYT database.
    first_page_prefix : str
        (under development) returns compute_n_pages() formatted as a string. 
    iterate_search_over_pages: requests.Response
        iterator that repeats a search over all available pages.
    set_date : None
        sets the date to which the search results will be limited.

    Usage
    -----
    nyt_api = NYTapi( preamble, search_base, query, key )
    nyt_api.set_date( date )
    for response in nyt_api.iterate_search_over_pages():
        write_to_file(data=response, filename=filename, write_mode='a')
    """
    hits_per_page = 10

    def __init__(self, preamble, search_base, query, key) :
        """
        """
        self.preamble = preamble
        self.search_base = search_base
        self.query = query
        self.key = key
        self.page = 0
        self.fq = ''
        self.date_set = False
        self.max_pages = 1000

    def url(self) :
        search = self.search_base.format(self.query,self.fq,self.page,self.key)
        return self.preamble + search

    def url_pretty(self) :
        return 'primary url = {0}'.format(self.url()) + '\n'

    def search(self) :
        return requests.get( self.url() ).text + '\n'

    def compute_n_pages( self, response_as_text ) :
        response_as_json = json.loads( response_as_text )
        n_hits = int(response_as_json['response']['meta']['hits'])
        return round(n_hits / self.hits_per_page + .5)

    def first_page_prefix( self, response ) :
        response_as_json = json.loads( response )
        n_hits = response_as_json['response']['meta']['hits']
        return "n_hits = {0}".format(n_hits) + '\n'

    def iterate_search_over_pages(self):
        stop = False
        self.page = 0
        while not stop:
            response = self.search()
            if self.page == 0:
                self.max_pages = self.compute_n_pages( response )
                response = self.first_page_prefix( response ) + response
            print("Querying page {0} of {1}".format(self.page, self.max_pages))
            print('url:\t', self.url(), '\n')
            time.sleep(6)
            self.page += 1
            if self.page > self.max_pages:
                break
            yield response

    def set_date(self, date) :
        self.fq = 'pub_date:({0})'.format(date)
        self.date_set = True
