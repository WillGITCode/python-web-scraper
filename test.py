import newspaper
from newspaper.utils import BeautifulSoup
import datetime
from dateutil.parser import parse
from services import webscrape_service, cache_service
from urllib.parse import urljoin, urlparse
from os import path
import json

webscrape_service = webscrape_service.WebScrapeService()

url = "https://www.sciencealert.com"
url2 = "https://futurespartan.com"





print("==========================")
print(urlparse(url).netloc.split(".")[-2])
print(urlparse(url2).netloc.split(".")[-2])
print("==========================")
