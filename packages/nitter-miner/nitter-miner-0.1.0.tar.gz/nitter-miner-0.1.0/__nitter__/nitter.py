#!/usr/bin/python3
from .nitter_scraper import nitter_scraper
import argparse
import os

msg = 'help/documentation:\n\thttps://github.com/hashirkz/twitter_scraper\n\tver 0.1.1\n\ndescription:\n\twebscraper for pulling tweets from...\n\t'
mirrors = [
    'https://nitter.net/search',
    'https://nitter.nicfab.eu/search',
    'https://nitter.privacydev.net/search',
    'https://tweet.whateveritworks.org/search'
]

msg += '\n\t'.join(mirrors) + '\n'

def app():
    parser = argparse.ArgumentParser(
        prog="nitter",
        description=msg
    )
    query_type = parser.add_mutually_exclusive_group(required=True)

    query_type.add_argument('-q', '--query')
    query_type.add_argument('-qf', '--query-file', dest='query_file')
    parser.add_argument('-p', '--pgs', default=50, type=int, help='max pgs to search on nitter.net')
    parser.add_argument('-m', '--mirror', dest='mirror', default='https://nitter.net/search')
    parser.add_argument('--retweets', dest='retweets', action='store_true')
    parser.add_argument('--no-sentiments', dest='senti', action='store_true')
    parser.add_argument('--no-save', dest='save', action='store_true')
    params = parser.parse_args()

    # defaults to true now
    params.senti, params.save = not params.senti, not params.save
    
    if not params.query and not params.query_file:
        print('ERROR: no supplied query or queryfile')
        return
    
    # if we want to dynamically search some different mirror
    nitter = nitter_scraper(_endpoint=params.mirror)
    if params.query:
        nitter.search(
            q=params.query, max_pgs=params.pgs, show_rt=params.retweets, 
            sentiments=params.senti, save=params.save)    

    else:
        # bmo,cibc,rbc,scotiabank,td = nitter_scraper.read_queries()
        # nitter.search_list(b=td, sentiments=True, max_pgs=50)
        for col in nitter_scraper.read_queries(params.query_file):
            nitter.search_list(b=col, max_pgs=params.pgs,
            sentiments=params.senti, save=params.save)

if __name__ == '__main__':
    app()