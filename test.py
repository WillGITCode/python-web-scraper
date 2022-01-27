import newspaper
from newspaper.utils import BeautifulSoup
import datetime
from dateutil.parser import parse
from services import webscrape_service

webscrape_service = webscrape_service.WebScrapeService()

links = webscrape_service.get_crawled_site_links("https://www.sciencealert.com/latest")


print("==========================")
print(len(links))
# print(links)
print("==========================")

# strings = ['https://nature.com', 'https://theconversation.com/profiles/kersten-hall-130291', 'https://theconversation.com/jobs/maisam-najafizada-427368', '/profiles/maria-josey-1300777']

# my_strings = list(filter(lambda x: x.find("/profiles/") > -1, strings))

# for i in range(len(my_strings)):
#     if my_strings[i].startswith("/"):
#         my_strings[i] = "https://theconversation.com" + my_strings[i]

# page_links = set((webscrape_service.get_crawled_page_links(strings[0])))

# print("==========================")
# print(page_links)
# print(len(page_links))
