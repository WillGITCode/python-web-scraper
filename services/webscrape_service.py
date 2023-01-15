
import time
from urllib.parse import urljoin, urlparse
from utilities.data_util import remove_list_duplicates
from utilities.site_content_util import SiteUtil
import random
from utilities import logger
from services import cache_service

class WebScrapeService:
    def __init__(self):
        self.site_util = SiteUtil()
        self.cache_service = cache_service.CacheService()

    # Checks whether `url` is a valid URL
    def link_is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    # Remove URL GET parameters, queries, fragments
    def remove_url_fragments(self, url):
        parsed_url = urlparse(url)
        
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        return clean_url

    def filter_urls(self, site_urls, includes=None, excludes=None):
        try:
            matching_urls = site_urls
            # If given includes add to matching urls
            if includes is not None and len(includes) > 0:
                for sub_string in includes:
                    matching_urls = list(filter(lambda x: x.find(sub_string) > -1, site_urls))
            # If given excludes remove from matching urls
            if excludes is not None and len(excludes) > 0:
                for sub_string in excludes:
                    matching_urls = list(filter(lambda x: x.find(sub_string) == -1, matching_urls))
            return matching_urls
        except:
            logger.error("Error: Could not filter urls")

    def get_recent_site_pages(self, url, date_range, sub_directories=None, exclude_directories=None):
        site_urls = self.get_crawled_site_urls(url, exclude_directories)
        filtered_urls = self.filter_urls(site_urls, sub_directories, exclude_directories)
        site_pages = self.site_util.get_pages(filtered_urls)
        recent_pages = self.site_util.filter_pages_by_publication_date(site_pages, date_range)
        return remove_list_duplicates(recent_pages)

    def load_page_content(self, page):
        try:
            page_content = self.site_util.load_page_content(page)
            return page_content
        except:
            logger.error("Error: Could not load page content")

    def get_crawled_page_links(self, url):
        try:
            # Get unique links from page
            page_links = list(self.site_util.scrape_page_link_urls(url))
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
            return relevent_links
        except:
            logger.error("Error: Could not crawl links at:" + url)
    
    def get_crawled_site_urls(self, url, exclude_directories=None):
        # Recursive function to crawl site
        def crawl(url):
            # Get current site links from page
            try:
                page_links = self.get_crawled_page_links(url)
                if page_links is not None:
                    logger.info("Crawling: " + url + " Current urls: " + str(len(unique_site_urls)))

                    for link in page_links:
                        # Invalid URL
                        if not self.link_is_valid(link):
                            continue
                        # Not unique
                        if link in unique_site_urls:
                            continue
                        # External link
                        if domain_name not in link:
                            continue
                        # Url includes blacklisted sub_directories
                        if [sub_dir for sub_dir in exclude_directories if(sub_dir in link)]: 
                        # exclude_directories is not None and link in exclude_directories:
                            continue
                        # Add to unique site links
                        unique_site_urls.add(link) 
                        # time.sleep(random.random()*6)
                        # Recursive call
                        crawl(link)
            except BaseException as error:
                logger.error("Error in crawls: " + str(error) + " " + str(type(error)))
                pass

        try:
            # Domain name of the URL
            domain_name = urlparse(url).netloc
            # Create an accumalated links set
            unique_site_urls = set(())
            # Check if site has a cached site map
            site_map = self.cache_service.get_site_cache(url)
            # If so add previously crawled links
            if site_map is not None and site_map["urls"] is not None:
                unique_site_urls.update(site_map["urls"])
            # Crawl site recursively
            crawl(url)
            site_urls = list(unique_site_urls)
            # Update cached site map
            self.cache_service.set_site_cache(url, site_urls)
            return site_urls
        except BaseException as error:
            logger.error("Error crawling site:" + str(error))