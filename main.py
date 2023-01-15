from pandas import date_range
import config as config
from services import webscrape_service, email_service
from utilities import logger

# Create service objects
email_service = email_service.EmailService(config)
webscrape_service = webscrape_service.WebScrapeService()
# Temp declare sites
sites = config.sites
keywords = config.keywords
date_range = config.date_range
url_black_list = config.url_black_list
log_level = config.log_level

# Entry point
def main():
    try:
        # Start logs
        logger.start_log(log_level)
        logger.info("Starting main")
        # Create email body to append to
        email_body = ""
        # Iterate through sites
        for site in sites:
            # Articles to summarize in email
            recent_pages = webscrape_service.get_recent_site_pages(site[0], date_range, site[1:], url_black_list)
            logger.info("recent articles: " + str(len(recent_pages)))
            for page in recent_pages:
                # Get article content
                page_content = webscrape_service.load_page_content(page)
                # If Article contains targeted keywords add to email body
                if page_content.keywords is not None and any(keyword in keywords for keyword in page_content.keywords):
                    article_paragraph = email_service.format_email_paragraph(page_content)
                    # And space
                    email_body += article_paragraph + "\n \n \n"

        # send email
        if len(email_body) > 0:
            email_service.send_email(email_service.format_email_subject(keywords), email_body)
    except BaseException as error:
        logger.error("Error excuting main: " + str(error) + " " + str(type(error)))


if __name__ == '__main__':
    main()