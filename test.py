from typing import List
import newspaper
from newspaper.utils import BeautifulSoup
import datetime
from dateutil.parser import parse
from services import webscrape_service, cache_service
from urllib.parse import urljoin, urlparse
from os import path
import json
from htmldate import find_date

webscrape_service = webscrape_service.WebScrapeService()

matching_urls = []

sub_string = "https://www.theguardian.com/us"

matching_urls = list(filter(lambda x: x.find(sub_string) == -1, matching_urls))

print(matching_urls)


print("==========================")
