import newspaper
from email_sender import send_email

# List of sites
sites = ["https://nature.com"]

def get_site(url):
    # Create site source object
    site = newspaper.build(url, memoize_articles=False)
    return site

def get_site_urls(site):
    # get list of article URLs
    return site.article_urls()

def get_site_articles(site):
    return site.articles

def get_site_article(site, index):
    return site.articles(index)
 
def get_article_content(article):
    # get content
    article.download()
    # parse HTML
    article.parse()
    # get list of image links
    article.images
    # get list of videos
    article.movies
    # process natural language (try to :)
    article.nlp()
    # keywords
    article.keywords
    return article



# first site
my_site = get_site(sites[0])
my_site_urls = get_site_urls(my_site)
my_site_articles = get_site_articles(my_site)
my_first_article = get_article_content(my_site_articles[0])

email_subject = ", ".join(my_first_article.keywords)
email_body = """\
    Article Title: %s
    Article URL: %s
    Article NLP summary: %s
    """ % (my_first_article.title, my_first_article.url, my_first_article.summary)


send_email(email_subject, email_body)


# Print findings
# print("========================")
# print("Article Title: " + )
# print("========================")
# print("Article URL:")
# print()
# print("========================")
# print("Article keywords:")
# print(my_first_article.keywords)
# print("========================")
# print("Article NLP summary:")
# print()
# print(" ")
#print(my_first_article.text)