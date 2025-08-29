# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *

# If your site is available via HTTPS, make sure SITEURL begins with https://
SITEURL = "http://localhost:8080"
RELATIVE_URLS = True 
TAGS_URL = "tags"
CATEGORIES_URL = "categories"
AUTHORS_URL = "authors"
ARCHIVES_URL = "archives"

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
CATEGORY_URL = "category/{slug}"
TAG_URL = "tag/{slug}"
AUTHOR_URL = "author/{slug}"



DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

# DISQUS_SITENAME = ""
# GOOGLE_ANALYTICS = ""