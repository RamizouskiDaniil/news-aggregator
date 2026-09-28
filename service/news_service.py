from news_parser.parsers.XML_parser import parse_rss
from news_parser.service.article_service import add_article_service
import logging
import psycopg

logger = logging.getLogger(__name__)

def update_news(config):
    article_data = parse_rss()
    if not article_data:
        logger.warning("No articles to update")
    else:
        for article in article_data:
            try:
                add_article_service(article, config)
            except psycopg.DatabaseError as e:
                logger.warning("Failed to add article, title - %s, link - %s, reason - %s", article.title, article.link, e )