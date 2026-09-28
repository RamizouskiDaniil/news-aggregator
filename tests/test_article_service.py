from news_parser.database.article_repository import add_article
from news_parser.models import Article
from news_parser.config import Config
from news_parser.database.connection import get_connection
import pytest
from datetime import datetime

@pytest.fixture
def article():
    return Article(
        id="ID test",
        title="title test",
        description="description test",
        link="link test",
        pubDate="2026-09-28 08:10:08",
        source="source test"
    )

@pytest.fixture
def config():
    return Config()


def test_add_article(article, config):
    add_article(article, config)
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM articles WHERE link = %s",
                ("link test",)
            )
            rows = cursor.fetchall()
            cursor.execute(
                "DELETE FROM articles WHERE link = %s",
                ("link test",))
            assert len(rows) == 1
            for row in rows:
                assert row[1] == "title test"
                assert row[2] == "description test"
                assert row[3] == "link test"
                assert row[4] == datetime(2026, 9, 28, 8, 10, 8)
                assert row[5] == "source test"

def test_duplicate_article(article, config):
    add_article(article, config)
    add_article(article, config)
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM articles WHERE link = %s",("link test",)
            )
            rows = cursor.fetchall()
            cursor.execute(
                "DELETE FROM articles WHERE link = %s",("link test",)
            )
            assert len(rows) == 1