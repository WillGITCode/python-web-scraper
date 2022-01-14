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
            # Build site
            site = webscrape_service.get_site(site)
            # Get articles
            site_articles = webscrape_service.get_site_articles(site)
            #site_articles = webscrape_service.get_recent_site_articles(site, config.publication_date)
            print(len(site_articles))
            # article_date = webscrape_service.get_article_publish_date(site_articles[0])
            for article in site_articles:
                print(article.url)
            #     # Get article content
            #     article_content = webscrape_service.get_article_content(article)
                # If Article contains targeted keywords
                # for keyword in article_content.keywords:
                #     print(keyword)
        #             # Add wanted article content to email body
        #             article_paragraph = email_service.format_email_paragraph(article_content)
        #             # And space
        #             email_body += article_paragraph + "\n \n \n"


            
        # # send email
        # email_service.send_email(email_service.format_email_subject(keywords), email_body)
    finally:
        print("Bye world!")


if __name__ == '__main__':
    main()