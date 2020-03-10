# Cache warmer
A Web Cache warmer to parse one or many websites based on one or multiple XML sitemaps.  
Written in Python 3.7 but works for any website (as long as a XML sitemap is available).

Based on [Bitnami's Python Docker image](https://github.com/bitnami/bitnami-docker-python) for convenience and small image size ;). 
## Usage and options
```
usage: cache-warmer.py [-h] [-t THREADS] [-u URL] [-f FILE] [-v]

Cache crawler based on a sitemap.xml URL (multiple URL are supported) or file
(only one file supported)

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        How many threads to use
  -u URL, --url URL     The sitemap xml url
  -f FILE, --file FILE  The sitemap xml file
  -v, --verbose         Be more verbose
```

## Examples

### With one or more URLs to XML sitemaps (using 4 threads)
Use the `-u` option to pass an URL.  
Separate multiple URL with commas: `-u url1,url2,url3`

```shell script
docker run kissmy/cache-warmer \
  -t 4 -v -u https://example.com/sitemapFR.xml,https://example.com/sitemapEN.xml,https://example.com/sitemapNL.xml
```

### With a local file
Use the `-f` option to pass a local file.  

```shell script
docker run kissmy/cache-warmer -t 1 -v -f /tmp/sitemap.xml
```

**Multiple local files are not supported**, only multiple urls as we don't have any use case for multiple files.  
Feel free to submit a PR or create an issue if you need this feature. 

## Available tags
Check [our Docker Hub page](https://hub.docker.com/r/kissmy/cache-warmer) for available tags. There's always a `latest` tag available **that points to the master branch** 


## Contributing
PR and enhancement ideas welcome.

## Thanks & Credits
### Contributors
[@superbiche](https://github.com/superbiche) migration to Python 3.7, add multiple URL support, Docker build and current maintainer.
### Special thanks
[Thanks to Hypernode Support for the initial Gist](https://gist.github.com/hn-support/bc7cc401e3603a848a4dec4b18f3a78d) that made our day.

## License
MIT