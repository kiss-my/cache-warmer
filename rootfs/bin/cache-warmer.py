#!/usr/bin/env python
"""
Warm the caches of your website by crawling each page defined in sitemap.xml (can use a local file or an URL).
To use, download this file and make it executable. Then run:
./cache-warmer.py --threads 4 --url http://example.com/sitemap.xml -v
"""
import argparse
import multiprocessing.pool as mpool
import os.path
import re
import sys
import time
import requests
import subprocess
import urllib.request, urllib.error, urllib.parse
from itertools import chain

results = []
start = time.time()


def parse_options():
    parser = argparse.ArgumentParser(description="""Cache crawler based on a sitemap.xml URL (multiple URL are supported) or file (only one file supported)""")
    parser.add_argument('-t', '--threads', help='How many threads to use', default=10, required=False, type=int)
    parser.add_argument('-u', '--url', help='The sitemap xml url', required=False, type=str)
    parser.add_argument('-f', '--file', help='The sitemap xml file', required=False, type=str)
    parser.add_argument('-v', '--verbose', help='Be more verbose', action='store_true', default=False)

    args = parser.parse_args()
    url_checks = []
    
    if args.url:
      if ',' in args.url:
        args.urls = args.url.split(',')
      else:
        args.urls = [args.url]
      try:
        url_checks = [requests.options(url).status_code for url in args.urls if args.url]
      except:
        pass

    if args.file and not os.path.isfile(args.file):
      parser.error('Could not find sitemap file %s' % args.file)
    elif args.url and not all(check == 200 for check in url_checks):
      for i, code in enumerate(url_checks):
        if code != 200:
          parser.error('Could not get sitemap from given URL: %s (Code: %d)' % (args.urls[i], code))
    return args

def crawl_url(url, verbose=False):
    if verbose:
        print("Crawling {}".format(url))
    a = requests.get(url, headers={"user-agent": "SitemapCacheWarmer"})
    return {'exit': 0 if a.ok() else 1, 'out': a.text, 'url': url}


def make_results():
    errcount = 0
    exec_time = format(time.time() - start, '.4f')
    for item in results:
        if item['exit'] == 0:
            continue
        else:
            errcount += 1
            print("Errors detected in %s:\n%s\n" % (item['url'], item['out']))
            print("=" * 50)
    if errcount == 0:
        print("All DONE! - All urls are warmed! - done in %s " % exec_time)
        return 0
    else:
        print("%d Errors detected! - done in %ss" % (errcount, exec_time))
        return 1


def get_sitemap_urls_from_file(filename):
    with open(filename) as fh:
        return re.findall('<loc>(.*?)</loc>?', fh.read())

def get_sitemap_urls_from_urls(urls):
    return list(chain.from_iterable(re.findall('<loc>(.*?)</loc>?', str(urllib.request.urlopen(url).read())) for url in urls))

def callback(output):
    results.append(output)


def main():
    args = parse_options()
    if args.file:
      sitemap_urls = get_sitemap_urls_from_file(args.file)
    else:
      sitemap_urls = get_sitemap_urls_from_urls(args.urls)

    if args.verbose:
        print("Crawling {} urls with {} threads\n[Please Wait!]".format(len(sitemap_urls), args.threads))
        print("=" * 50)

    pool = mpool.ThreadPool(args.threads)
    for url in sitemap_urls:
        pool.apply_async(crawl_url, args=(url,), callback=callback)
    pool.close()
    pool.join()
    sys.exit(make_results())      


if __name__ == "__main__":
    main()