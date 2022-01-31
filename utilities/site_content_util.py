import newspaper
from htmldate import find_date
import datetime
import json
from newspaper.utils import BeautifulSoup
from dateutil.parser import parse



class SiteUtil:
    # newspaper based functions
    def build_site(self, url):
        try:
            return newspaper.build(url, memoize_articles=False)
        except:
            print("Error: Could not get page object")

    def get_page(self, url):
        try:
            return newspaper.Article(url)
        except:
            print("Error: Could not get page object")

    def get_pages(self, urls):
        try:
            return [self.get_page(url) for url in urls]
        except:
            print("Error: Could not get pages")

    def get_basic_site_article_urls(self, site):
        # get list of article URLs
        try:
            return site.article_urls()
        except:
            print("Error: Could not get list of article URLs")

    def scrape_page_link_urls(self, url):
        try:
            site = newspaper.build(url, memoize_articles=False)
            # parse HTML
            site_mark_up = BeautifulSoup(site.html, 'html.parser')
            site_page_link_urls = []
            # get links
            for link in site_mark_up.find_all('a'):
                # get link ref
                href = link.attrs.get("href")
                if href == "" or href is None:
                # skip empty href tag
                    continue
                # populate list
                site_page_link_urls.append(href)
            return site_page_link_urls
        except:
            print("Error: Could not scrape page link at: ", url)

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

    def filter_pages_by_publication_date(self, pages, published):
        recent_pages = []
        if pages is not None:
            for page in pages:
                try:
                    publication_cutoff = datetime.date.today() 
                    if published is not None and published > 0: 
                        publication_cutoff = publication_cutoff - datetime.timedelta(days=published)
                    
                    publication_date_value = self.get_page_publish_date(page)
                    # Skip if page publish date is not found
                    if publication_date_value is None:
                        continue
                    publish_date = parse(publication_date_value).date()
                    if(publish_date > publication_cutoff):
                        print(page.url, ":", publish_date)
                        recent_pages.append(page)
                    
                except:
                    print("Error: Could not get recent articles")
        return recent_pages
    
    # def get_page_publish_date(self, page):
    #     try:
    #         # get content
    #         page.download()
    #         # parse HTML
    #         page.parse()
    #         print(page.url)
    #         soup = BeautifulSoup(page.html, 'html.parser')
    #         # print(soup)
            
    #         bbc_dictionary = json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
    #         publish_date = [value for (key, value) in bbc_dictionary.items() if (key == 'datePublished' or key == 'datePosted')]
    #         return publish_date
    #     except:
    #         print("Error: Could not get article publish date")

    def get_page_publish_date(self, page):
        try:
            # get content
            page.download()
            # parse HTML
            page.parse()
            publish_date = find_date(page.html)
            return publish_date
        except:
            print("Error: Could not get article publish date")

    def load_page_content(self, page):
        try:
            page.nlp()
            page.keywords
        except BaseException as err:
            if type(err) == newspaper.article.ArticleException:
                page.download()
                page.parse()
                page.nlp()
                page.keywords
        finally:
            return page
