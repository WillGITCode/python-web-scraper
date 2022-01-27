import newspaper
from urllib.parse import urljoin, urlparse
from newspaper.utils import BeautifulSoup
import json
import datetime
from dateutil.parser import parse

class WebScrapeService:
    # Checks whether `url` is a valid URL
    def link_is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    # Remove URL GET parameters, queries, fragments
    def remove_url_fragments(self, url):
        parsed_url = urlparse(url)
        
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        return clean_url

    # newspaper based functions
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
            print("Error: Could not scrape page link urls")

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

    def filter_recent_site_articles(self, site, date):
        
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

    # Custom/brute force based functions

    def get_crawled_page_links(self, url):
        try:
            # Get unique links from page
            page_links = list(self.scrape_page_link_urls(url))
            # Create an accumalated links set
            relevent_links = set(())
            # Add absolute links of current site
            relevent_links.update(list(filter(lambda x: x.find(url) > -1, page_links)))
            # And the links with relative links of current site
            relevent_links.update(list(filter(lambda x: x.startswith("/"), page_links)))
            # Convert set to list for iteration
            relevent_links = list(relevent_links)
            # Make every link URL absolute
            for i in range(len(relevent_links)):
                if relevent_links[i].startswith("/"):
                    relevent_links[i] = urljoin(url,relevent_links[i])

            return list(relevent_links)
        except:
            print("Error: Could not crawl page links")
    
    def get_crawled_site_links(self, url):
        # Recursive function to crawl site
        def crawl(url):
            # Get current site links from page
            page_links = self.get_crawled_page_links(url)
            print("New urls at:", url, len(page_links))
            print("Total urls:", len(unique_site_links))

            for link in page_links:
                # Invalid URL
                if not self.link_is_valid(link):
                    continue
                # Not unique
                if link in unique_site_links:
                    continue
                # External link
                if domain_name not in link:
                    continue
                # Add to unique site links
                unique_site_links.add(link) 
                # Recursive call
                crawl(link)

        try:
            # Domain name of the URL
            domain_name = urlparse(url).netloc
            # Create an accumalated links set
            unique_site_links = set(())
            # Crawl site
            crawl(url)
    
            return list(unique_site_links)
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")

             # for article in site_articles:
            #     print(article.url)
            #     # Get article content
            #     article_content = webscrape_service.get_article_content(article)
                # If Article contains targeted keywords
                # for keyword in article_content.keywords:
                #     print(keyword)
        #             # Add wanted article content to email body
        #             article_paragraph = email_service.format_email_paragraph(article_content)
        #             # And space
        #             email_body += article_paragraph + "\n \n \n"