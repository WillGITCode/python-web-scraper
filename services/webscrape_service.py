import newspaper
from newspaper.utils import BeautifulSoup
import json
import datetime
from dateutil.parser import parse

class WebScrapeService:
      
    def get_site(self, url):
        # Create site source object
        try:
            site = newspaper.build(url, memoize_articles=False)
            return site
        except:
            print("Error: Could not build site source object")

    def get_basic_site_article_urls(self, site):
        # get list of article URLs
        try:
            return site.article_urls()
        except:
            print("Error: Could not get list of article URLs")

    def scape_page_link_urls(self, url):
        try:
            site = newspaper.build(url, memoize_articles=False)
            # parse HTML
            soup = BeautifulSoup(site.html, 'html.parser')
            soupArticles = []
            for link in soup.find_all('a'):
                soupArticles.append(link.get('href'))
        except:
            print("Error: Could not scape page link urls")

    def get_site_articles(self, site):
        try:
            return site.articles
        except:
            print("Error: Could not get list of articles")

    def get_site_article(self, site, index):
        try:
            return site.articles(index)
        except: 
            print("Error: Could not get article")

    def get_recent_site_articles(self, site, date):
        
        recent_articles = []
        for article in site.articles:
            try:
                publish_date = parse(self.get_article_publish_date(article)[0]).date()
                today = datetime.date.today()
                print("publish_date : ", publish_date)
                print("today : ", today)
                print("recent : ", today < publish_date)
                # if(publish_date.date() > today.date()):
                #     recent_articles.append(article)
                # return recent_articles
            except:
                print("Error: Could not get recent articles")
    
    def get_article_publish_date(self, article):
        try:
            # get content
            article.download()
            # parse HTML
            article.parse()

            soup = BeautifulSoup(article.html, 'html.parser')
            
            bbc_dictionary = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
            publish_date = [value for (key, value) in bbc_dictionary.items() if (key == 'datePublished' or key == 'datePosted')]
            return publish_date
        except:
            print("Error: Could not get article publish date")

    def get_article_content(self, article):
        try:
            # get content
            article.download()
            # parse HTML
            article.parse()
            # get list of image links
            article.images
            # try get date
            article.publish_date = self.get_article_publish_date(article)
            # get list of videos
            article.movies
            # process natural language (try to :)
            article.nlp()
            # keywords
            article.keywords
            return article
        except:
            print("Error: Could not get article content")