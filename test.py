import newspaper
from newspaper.utils import BeautifulSoup
import json
import datetime
from dateutil.parser import parse

strings = ['https://theconversation.com/profiles/kersten-hall-130291', 'https://theconversation.com/jobs/maisam-najafizada-427368', '/profiles/maria-josey-1300777']

my_strings = list(filter(lambda x: x.find("/profiles/") > -1, strings))

for i in range(len(my_strings)):
    if my_strings[i].startswith("/"):
        my_strings[i] = "https://theconversation.com" + my_strings[i]

print(my_strings)