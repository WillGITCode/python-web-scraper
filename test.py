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

url = "https://www.sciencealert.com"
url2 = "https://futurespartan.com/dynamic-spfx-webpart-layouts-using-handlebars"
url3 = "https://futurespartan.com/cdn-cgi/l/email-protection#94e1e7f1e6faf5f9f1d4f0fbf9f5fdfabafbfaf9fdf7e6fbe7fbf2e0baf7fbf9"


# page = newspaper.Article(url2)
# page.download()
# page.parse()
# page.nlp()


# List1
List1 = ['python' ,  'javascript', 'csharp', 'go', 'c', 'c++']
 
# List2
List2 = ['csharp1' , 'go', 'python']

check =  any(item in List1 for item in List2)
 
if check is True:
    print("The list {} contains all elements of the list {}".format(List1, List2))    
else :
    print("No, List1 doesn't have all elements of the List2.")

print("==========================")
print("==========================")
