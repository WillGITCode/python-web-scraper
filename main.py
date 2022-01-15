import config as config
from services import email_service
from services import webscrape_service

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
            # Get links present on site page
            page_links = webscrape_service.scrape_page_link_urls(site[0])
            print("Links present on page", site[0] ,len(page_links))
            relevent_links = []
            # Limit to relevent links By subpaths
            if len(site) > 1:
                for path in site[1:]:
                    links_at_path = list(filter(lambda x: x.find(path) > -1, page_links))
                    print(len(links_at_path), " links with subpath", path)
                    relevent_links.extend(links_at_path)
            # Or by the current pages URL
            else:
                print("No path specified")
                relevent_links.extend(list(filter(lambda x: x.find(site[0]) > -1, page_links)))
                # And the links with relative paths present on the page
                relevent_links.extend(list(filter(lambda x: x.startswith("/"), page_links)))

            # Make every link URL absolute
            for i in range(len(relevent_links)):
                if relevent_links[i].startswith("/"):
                    relevent_links[i] = site[0] + relevent_links[i]

            print("Relevent links : ", len(relevent_links))
            print (relevent_links)


            
        # # send email
        # email_service.send_email(email_service.format_email_subject(keywords), email_body)
    finally:
        print("Bye world! \n")


if __name__ == '__main__':
    main()