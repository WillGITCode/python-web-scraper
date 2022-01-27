import config as config
from services import webscrape_service, cache_service, email_service

# Create service objects
email_service = email_service.EmailService(config)
webscrape_service = webscrape_service.WebScrapeService()
# Temp declare sites
sites = config.sites
keywords = config.keywords

# Entry point
def main():
    try:
        email_body = ""
        # Iterate through sites
        for site in sites:
            # Declare the list of urls
            site_urls = []
            # Check if site has a cached file with content
            site_cache_file_name = cache_service.cache_file_name_from_url(site[0])
            site_has_cached_urls = cache_service.file_has_key(site_cache_file_name ,"urls")
            if cache_service.file_exists(site_cache_file_name) and site_has_cached_urls:
                # Update list with sites cached urls
               site_urls = cache_service.get_file_contents(site_cache_file_name)["urls"]
            else:
                # Crawl site from scratch
                # site_urls = webscrape_service.get_crawled_site_urls(site[0])
                print("no cache")
            print("Links found at site", site[0] ,len(site_urls))
            relevent_links = []
            # Limit to relevent links By subpaths
            if len(site) > 1:
                for path in site[1:]:
                    links_at_path = list(filter(lambda x: x.find(path) > -1, site_urls))
                    print(len(links_at_path), " links with subpath", path)
                    relevent_links.extend(links_at_path)
            # Or all links
            else:
                print("No path specified")
                relevent_links = site_urls

            print("Relevent links : ", len(relevent_links))
            # print (relevent_links)


            
        # # send email
        # email_service.send_email(email_service.format_email_subject(keywords), email_body)
    finally:
        print("Bye world! \n")


if __name__ == '__main__':
    main()