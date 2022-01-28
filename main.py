import config as config
from services import webscrape_service, email_service

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
            # Articles to summarize in email
            recent_articles = webscrape_service.get_recent_site_content(site[0], "today", site[1:])

            print("recent articles", len(recent_articles))

            
        # # send email
        # email_service.send_email(email_service.format_email_subject(keywords), email_body)
    finally:
        print("Bye world! \n")


if __name__ == '__main__':
    main()