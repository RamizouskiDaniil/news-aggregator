from news_parser.parsers.XML_parser import parse_articles, fetch_rss
import xml.etree.ElementTree as ET
import pytest
import logging
import requests, builtins
import io
from news_parser.service import news_service
from news_parser.service.news_service import update_news
from news_parser import config
import psycopg
from news_parser.models import Article


@pytest.fixture
def valid_article():
    return ET.fromstring("""<item>
     <title>
    <![CDATA[ Hadjar set to make Red Bull return at Azerbaijan GP after injury recovery ]]> 
    </title> 
    <link>https://www.autosport.com/f1/news/hadjar-to-make-red-bull-return-in-baku/10857880/?utm_source=RSS&amp;utm_medium=referral&amp;utm_campaign=RSS-F1&amp;utm_term=News&amp;utm_content=uk</link> 
    <description> <![CDATA[ Isack Hadjar will return to Red Bull for this weekend's Azerbaijan Grand Prix at Baku after recovering from a wrist injury, as Liam Lawson moves back to the Racing Bulls Formula 1 team.<br>Hadjar had injured his wrist in training over the summer break and, following medical advice, was told to avoid driving to manage his recovery.<br>Lawson therefore deputised for the Frenchman at Red Bull ...<a class='more' href='https://www.autosport.com/f1/news/hadjar-to-make-red-bull-return-in-baku/10857880/?utm_source=RSS&utm_medium=referral&utm_campaign=RSS-F1&utm_term=News&utm_content=uk'>Keep reading</a> ]]> </description> 
    <category>Baku City Circuit</category> 
    <category>Formula 1</category> 
    <guid isPermaLink="false">10857880</guid> 
    <pubDate>Tue, 22 Sep 2026 08:33:19 +0000</pubDate> 
    <enclosure url="https://cdn-4.motorsport.com/images/amp/Y9lNNNX2/s6/isack-hadjar-red-bull-racing-3.jpg" type="image/jpeg" length="216097"/> </item>""")

def test_parse_articles(valid_article):
    article = [(valid_article,"Autosport")]

    parsed_article = parse_articles(article)

    assert len(parsed_article) == 1
    assert parsed_article[0].title == "\n     Hadjar set to make Red Bull return at Azerbaijan GP after injury recovery  \n    "
    assert parsed_article[0].link == "https://www.autosport.com/f1/news/hadjar-to-make-red-bull-return-in-baku/10857880/?utm_source=RSS&utm_medium=referral&utm_campaign=RSS-F1&utm_term=News&utm_content=uk"
    assert parsed_article[0].pubDate == "Tue, 22 Sep 2026 08:33:19 +0000"
    assert parsed_article[0].source == "Autosport"

def test_parse_article_without_title(valid_article, caplog):
    caplog.set_level(logging.WARNING)
    title = valid_article.find("title")
    valid_article.remove(title)
    article = [(valid_article,"Autosport")]

    parsed_article = parse_articles(article)

    assert len(parsed_article) == 0
    assert "Title not found" in caplog.text

def test_parse_article_without_link(valid_article, caplog):
    caplog.set_level(logging.WARNING)
    link = valid_article.find("link")
    valid_article.remove(link)
    article = [(valid_article,"Autosport")]

    parsed_article = parse_articles(article)

    assert len(parsed_article) == 0
    assert "Link not found" in caplog.text

def test_parse_article_without_description(valid_article, caplog):
    caplog.set_level(logging.WARNING)
    description = valid_article.find("description")
    valid_article.remove(description)
    article = [(valid_article,"Autosport")]

    parsed_article = parse_articles(article)

    assert len(parsed_article) == 1
    assert parsed_article[0].description is None
    assert "Description not found" in caplog.text

def test_parse_article_without_pub_date(valid_article, caplog):
    caplog.set_level(logging.WARNING)
    pubDate = valid_article.find("pubDate")
    valid_article.remove(pubDate)
    article = [(valid_article,"Autosport")]

    parsed_article = parse_articles(article)

    assert len(parsed_article) == 0
    assert "PubDate not found" in caplog.text

def test_parse_article_without_source(valid_article, caplog):
    caplog.set_level(logging.WARNING)
    article = [(valid_article,"")]
    parsed_article = parse_articles(article)

    assert len(parsed_article) == 0
    assert "Source not found" in caplog.text

def test_fetch_rss(monkeypatch):
    monkeypatch.setattr(requests, "get",fake_get)
    monkeypatch.setattr(builtins, "open", fake_open)
    result = fetch_rss()
    assert len(result) == 1
    assert result[0][1] == "HackerNews"
    assert isinstance(result[0][0], ET.Element)

def test_fetch_rss_timeout(monkeypatch, caplog):
    caplog.set_level(logging.ERROR)
    monkeypatch.setattr(requests, "get",fake_get_timeout)
    monkeypatch.setattr(builtins, "open", fake_open)
    result = fetch_rss()
    assert result == []
    assert "Timeout while fetching RSS" in caplog.text

def test_fetch_rss_request_exception(monkeypatch, caplog):
    caplog.set_level(logging.ERROR)
    monkeypatch.setattr(requests, "get",fake_get_request_exception)
    monkeypatch.setattr(builtins, "open", fake_open)
    result = fetch_rss()
    assert result == []
    assert "Request failed for" in caplog.text

def test_fetch_rss_parse_error(monkeypatch, caplog):
    caplog.set_level(logging.ERROR)
    monkeypatch.setattr(requests, "get",fake_get_parse_error)
    monkeypatch.setattr(builtins, "open", fake_open)
    result = fetch_rss()
    assert result == []
    assert "Parse error for" in caplog.text

def test_fetch_rss_without_channel(monkeypatch, caplog):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr(builtins, "open", fake_open)
    monkeypatch.setattr(requests, "get",fake_get_without_channel)
    result = fetch_rss()
    assert result == []
    assert "Channel not found" in caplog.text

def test_fetch_rss_without_item(monkeypatch, caplog):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr(builtins, "open", fake_open)
    monkeypatch.setattr(requests, "get",fake_get_without_item)
    result = fetch_rss()
    assert result == []
    assert "Item not found" in caplog.text

def test_update_news(monkeypatch):
    articles = []

    def fake_add_article_service(article, config):
        articles.append(article)
    monkeypatch.setattr(news_service, "parse_rss",fake_parse_items)
    monkeypatch.setattr(news_service,"add_article_service",fake_add_article_service)
    update_news(config)
    assert len(articles) == 3
    assert articles[0] == "BBC News"
    assert articles[1] == "Autosport"
    assert articles[2] == "HackerNews"

def test_update_news_without_articles(monkeypatch,caplog):
    articles = []
    caplog.set_level(logging.WARNING)

    def fake_add_article_service(article, config):
        articles.append(article)
    monkeypatch.setattr(news_service, "parse_rss",fake_parse_empty_items)
    monkeypatch.setattr(news_service,"add_article_service",fake_add_article_service)
    update_news(config)
    assert len(articles) == 0
    assert "No articles to update" in caplog.text

def test_update_news_with_database_error(monkeypatch,caplog):
    articles = []
    caplog.set_level(logging.WARNING)
    counter = 0
    def fake_add_article_service(article, config):
        nonlocal counter
        counter += 1
        if counter == 1:
            raise psycopg.DatabaseError("Database error")
        else:
            articles.append(article)
    monkeypatch.setattr(news_service, "parse_rss", fake_parse_items_with_articles)
    monkeypatch.setattr(news_service, "add_article_service", fake_add_article_service)
    update_news(config)
    assert len(articles) == 2
    assert "Failed to add article, title - test, link - test, reason - Database error" in caplog.text


def fake_parse_items():
    items = ["BBC News","Autosport","HackerNews"]
    return items

def fake_parse_items_with_articles():
    return [
        Article("BBC News", "test", "test", "test", "test", "test"),
        Article("Autosport", "test", "test", "test", "test", "test"),
        Article("HackerNews", "test", "test", "test", "test", "test")
    ]

def fake_parse_empty_items():
    items = []
    return items

def fake_get_without_item(url, timeout=10):
    return Fake_Response_Without_Item()


def fake_get(url, timeout=10):
    return Fake_Response()

def fake_get_without_channel(url, timeout=10):
    return Fake_Response_Without_Channel()

def fake_get_timeout(url, timeout=10):
    raise requests.exceptions.Timeout

def fake_get_request_exception(url, timeout=10):
    raise requests.exceptions.RequestException

def fake_get_parse_error(url, timeout=10):
    raise ET.ParseError

class Fake_Response:
    content = b"""<rss>
    <channel>
        <item>
            <title>Test article</title>
        </item>
    </channel>
</rss>"""

    def raise_for_status(self):
        pass

class Fake_Response_Without_Channel:
    content = b"""<rss>
            <item>
                <title>Test article</title>
            </item>
    </rss>"""

    def raise_for_status(self):
        pass

class Fake_Response_Without_Item:
    content = b"""<rss>
        <channel>
                <title>Test article</title>
        </channel>
    </rss>"""

    def raise_for_status(self):
        pass

def fake_open(path,mode):
    string = io.StringIO("HackerNews | https://news.ycombinator.com/rss")
    return string
