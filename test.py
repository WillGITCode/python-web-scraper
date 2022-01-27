import newspaper
from newspaper.utils import BeautifulSoup
import datetime
from dateutil.parser import parse
from services import webscrape_service
from urllib.parse import urljoin, urlparse
from os import path
import json

webscrape_service = webscrape_service.WebScrapeService()

url = "https://futurespartan.com"

links = webscrape_service.get_crawled_site_links(url)


site_map_json = {
    "urls": list(links)
}

write_file = urlparse(url).netloc
write_path = "./site_cache/" + write_file +".json"
write_path = path.abspath(write_path)

with open(write_path, "w") as write_file:
    json.dump(site_map_json, write_file)

print("==========================")
print(len(links))
print("==========================")
