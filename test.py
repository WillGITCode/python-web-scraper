import newspaper
from newspaper.utils import BeautifulSoup
import json
import datetime
from dateutil.parser import parse

def get_article_content():
    try:
        url = "https://www.nature.com/articles/d41586-022-00027-4"
        sub_paths = "/articles/"
        site = newspaper.build(url, memoize_articles=False)
        print(len(site.articles))
        # for article in site.articles:
        #     print(article.url)

        soup = BeautifulSoup(site.html, 'html.parser')
        soupArticles = []
        for link in soup.find_all('a'):
            # print(link.get('href'))
            if(link.get('href').find(sub_paths) > -1):
                soupArticles.append(link.get('href'))
        print(len(soupArticles))
        print(site.article_urls())
        print(" ")
        print(soupArticles)
    except:
        print("Error: Could not get article content")

get_article_content()