import xml.etree.ElementTree as ET
import requests
from news_parser.models.models import Article
import logging
logger = logging.getLogger(__name__)


def parse_rss():
    items = fetch_rss()
    return parse_articles(items)

def fetch_rss():
    items = []
    with open("RSS/rss_sourses.txt", "r") as file:
        parts = file.read()
        lines = parts.split("\n")
        for line in lines:
            part = line.split("|")
            source = part[0].strip()
            url = part[1].strip()
            try:
                xml = requests.get(url,timeout=10)
                xml.raise_for_status()

                root = ET.fromstring(xml.content)

                channel = root.find("channel")

                if channel is None:
                    logger.warning("Channel not found: %s", url)
                    continue

                item = channel.findall("item")

                if not item:
                    logger.warning("Item not found: %s", url)

            except requests.exceptions.Timeout:
                logger.error("Timeout while fetching RSS: %s",url)
                continue

            except requests.exceptions.RequestException as e:
                logger.error("Request failed for %s: %s",url,e)
                continue

            except ET.ParseError as e:
                logger.error("Parse error for %s: %s",url,e)
                continue

            for article in item:
                items.append((article, source))


        return items

def parse_articles(articles):
    article_data = []

    for article, source in articles:
        title = article.findtext("title")
        if not title:
            logger.warning("Title not found: %s",source)
            continue

        link = article.findtext("link")
        if not link:
            logger.warning("Link not found: %s",source)
            continue

        description = article.findtext("description")
        if not description:
            logger.warning("Description not found: %s",source)

        pubDate = article.findtext("pubDate")
        if not pubDate:
            logger.warning("PubDate not found: %s",source)
            continue

        if not source:
            logger.warning("Source not found: %s",title)
            continue

        article_obj = Article(
            title = title,
            link = link,
            description = description,
            pubDate = pubDate,
            source = source,
            id = id
        )

        article_data.append(article_obj)
    return article_data