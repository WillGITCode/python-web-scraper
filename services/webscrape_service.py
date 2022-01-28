
from urllib.parse import urljoin, urlparse
from utilities.data_util import remove_list_duplicates
from utilities.site_util import SiteUtil
from services import cache_service

class WebScrapeService:
    def __init__(self):
        self.site_util = SiteUtil()

    # Checks whether `url` is a valid URL
    def link_is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    # Remove URL GET parameters, queries, fragments
    def remove_url_fragments(self, url):
        parsed_url = urlparse(url)
        
        clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        return clean_url

    def get_site_map(self, url):
        # site's local file name
        cache_file_name = cache_service.cache_file_name_from_url(url)
        site_map = cache_service.get_file_contents(cache_file_name)
        return site_map

    def set_site_map(self, url, key, value):
        try:
            site_map = self.get_site_map(url)
            site_map[key] = value
            cache_service.set_file_contents(cache_service.cache_file_name_from_url(url), site_map)
        except:
            print("Error: Could not set site map")

#TODO: refactor and move to data_util
    def filter_urls_by_sub_directory(self, site_urls, sub_directories):
        try:
            matching_urls = []
            # If given sub_directories filter
            if sub_directories is not None and len(sub_directories) > 0:
                for directory in sub_directories:
                    links_at_directory = list(filter(lambda x: x.find(directory) > -1, site_urls))
                    print(len(links_at_directory), " links in directory", directory)
                    matching_urls.extend(links_at_directory)
            # Or return all
            else:
                print("No directory specified")
                return site_urls
            return matching_urls
        except:
            print("Error: Could not filter urls by sub directory")

    def get_recent_site_content(self, url, published, sub_directories=None):
        site_urls = self.get_crawled_site_urls(url)
        site_urls = self.filter_urls_by_sub_directory(site_urls, sub_directories)
        # site_urls = self.fi
        print("Relevent links : ", len(site_urls))
        return remove_list_duplicates(site_urls)

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

            return list(relevent_links)
        except:
            print("Error: Could not crawl page links")
    
    def get_crawled_site_urls(self, url):
        # Recursive function to crawl site
        def crawl(url):
            # Get current site links from page
            page_links = self.get_crawled_page_links(url)
            print("New urls at:", url, len(page_links))
            print("Total urls:", len(unique_site_urls))

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
                # Add to unique site links
                unique_site_urls.add(link) 
                # Recursive call
                crawl(link)

        try:
            # Domain name of the URL
            domain_name = urlparse(url).netloc
            # Create an accumalated links set
            unique_site_urls = set(())
            # Check if site has a cached site map
            site_map = self.get_site_map(url)
            # If so add previously crawled links
            if site_map is not None and site_map["urls"] is not None:
                unique_site_urls.update(site_map["urls"])
            # Crawl site recursively
            crawl(url)
            site_urls = list(unique_site_urls)
            # Update cached site map
            self.set_site_map(url, "urls", site_urls)
            return site_urls
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