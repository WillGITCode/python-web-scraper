import json
import requests
import pandas as pd
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
           
def query_foxbaltimore_news():
    df_foxbaltimore_extraction = pd.DataFrame(columns=['article_category', 'date_published', 'article authors',
                                                       'article title', 'article summary', 'article keywords',
                                                       'article url', 'article text'])

    url = 'http://nature.com/'
    response = requests.get(url, headers=HEADERS, allow_redirects=True, verify=True, timeout=30)
    soup = BeautifulSoup(response.content, 'html.parser')
    fox_soup = soup.find_all("script", {"type": "application/json"})[1]
    fox_json = json.loads(''.join(fox_soup))
    for news in fox_json['content']['page-data']['teaser']:
        for article in news['teasers']:
            article_category = article['categories'][0]
            article_title = article['title']
            article_url = f"https://foxbaltimore.com{article['url']}"
            article_summary = article['summary']
            article_published_date = article['publishedDateISO8601']
            if 'sponsored' not in article_url:
                article_details = query_individual_article_elements(article_url)
                df_foxbaltimore_extraction = df_foxbaltimore_extraction.append({'article category':article_category,
                                                                       'date_published': article_published_date,
                                                                       'article authors': article_details[0],
                                                                       'article title': article_title,
                                                                       'article summary': article_summary,
                                                                       'article keywords': article_details[3],
                                                                       'article url': article_url,
                                                                       'article text': article_details[5]}, ignore_index=True)
    print(df_foxbaltimore_extraction)
    return df_foxbaltimore_extraction


def query_individual_article_elements(url):
    config = Config()
    config.headers = HEADERS
    config.request_timeout = 30
    article = Article(url, config=config, memoize_articles=False)
    article.download()
    article.parse()
    article_meta_data = article.meta_data

    article_author = article.authors

    article_published_date = str({value['published_time'] for (key, value) in article_meta_data.items()
                                  if key == 'article'})

    article_keywords = sorted([value.lower() for (key, value) in article_meta_data.items() if key == 'keywords'])

    article_title = str({value for (key, value) in article_meta_data.items() if key == 'title'})

    article_summary = {value for (key, value) in article_meta_data.items() if key == 'description'}

    soup = BeautifulSoup(article.html, 'html.parser')
    fox_soup = soup.find_all("script", {"type": "application/json"})[1]
    fox_json = json.loads(''.join(fox_soup))
    article_text = ''.join(fox_json['content']['main_content']['story']['richText'])
    article_details = [article_author,
                       article_published_date,
                       article_title,
                       article_keywords,
                       article_summary,
                       article_text]

    return article_details

query_foxbaltimore_news()