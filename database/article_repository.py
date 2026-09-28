from .connection import get_connection
from ..models import Favorite, Article
import datetime
import logging
import psycopg

logger = logging.getLogger(__name__)


def create_main_table(config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            link TEXT NOT NULL UNIQUE,
            pubDate TIMESTAMP,
            source TEXT
            )
            """)

def add_article(article,config):
    try:
        with get_connection(config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO articles
                    (title, description, link, pubDate, source)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO NOTHING
                    """,
                    (
                        article.title,
                        article.description,
                        article.link,
                        article.pubDate,
                        article.source
                    )
                )

                if cursor.rowcount == 0:
                    logger.warning(
                        "Article already exists: %s",
                        article.link
                    )

    except psycopg.DatabaseError as error:
        logger.error("Database error: %s", error)
        raise


def get_articles(source,page,limit,sort,config):
    offset = (page - 1) * limit
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            if source is None:
                if sort:
                    cursor.execute(f"""
                                    SELECT id, title, description, link, pubDate, source 
                                    FROM articles
                                    ORDER BY {sort}
                                    LIMIT %s OFFSET %s""", (limit, offset))
                else:
                    cursor.execute("""
                                    SELECT id, title, description, link, pubDate, source 
                                    FROM articles
                                    ORDER BY pubDate DESC
                                    LIMIT %s OFFSET %s""", (limit, offset))
            else:
                if sort:
                    cursor.execute(f"""
                                    SELECT id, title, description, link, pubDate, source 
                                    FROM articles
                                    WHERE source = %s
                                    ORDER BY {sort}
                                    LIMIT %s OFFSET %s""", (source, limit, offset))
                else:
                    cursor.execute("""
                                    SELECT id, title, description, link, pubDate, source 
                                    FROM articles
                                    WHERE source = %s
                                    ORDER BY pubDate DESC
                                    LIMIT %s OFFSET %s""", (source, limit, offset))
            rows = cursor.fetchall()
            articles = []
            for row in rows:
                article = Article(
                    id = row[0],
                    title = row[1],
                    description = row[2],
                    link = row[3],
                    pubDate = row[4],
                    source = row[5],
                )
                articles.append(article)
    return articles

def get_articles_count(source,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            if source is None:
                count = cursor.execute("""SELECT COUNT(*) FROM articles""").fetchone()[0]
            else:
                count = cursor.execute("""SELECT COUNT(*) FROM articles WHERE source = %s""", (source,)).fetchone()[0]
    return count

def get_article_by_id(id,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, link, pubDate, source
                FROM articles
                WHERE id = %s
            """, (id,))

            row = cursor.fetchone()

            if row is None:
                return None

            article = Article(
                id=row[0],
                title=row[1],
                description=row[2],
                link=row[3],
                pubDate=row[4],
                source=row[5],
            )

            return article

def get_articles_by_date(date,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(f"""SELECT * from articles WHERE pubDate > now() - interval '{date}' ORDER BY pubDate DESC""")
            rows = cursor.fetchall()
            articles = []
            for row in rows:
                article = Article(
                    id = row[0],
                    title=row[1],
                    description=row[2],
                    link=row[3],
                    pubDate=row[4],
                    source=row[5],
                )
                articles.append(article)
    return articles

def get_latest_articles(config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
            """select id, title, description, link, pubDate, source from articles
            WHERE pubDate > now() - interval '7 days'
            ORDER BY pubDate DESC"""
            )
            rows = cursor.fetchall()
            articles = []
            for row in rows:
                article = Article(
                    id = row[0],
                    title=row[1],
                    description=row[2],
                    link=row[3],
                    pubDate=row[4],
                    source=row[5],
                )
                articles.append(article)
    return articles

def search_articles(query,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""select id, title, description, link, pubDate, source from articles
            WHERE title ILIKE %s OR description ILIKE %s""", (f'%{query}%',f'%{query}%'))
            rows = cursor.fetchall()
            articles = []
            for row in rows:
                article = Article(
                    id = row[0],
                    title=row[1],
                    description=row[2],
                    link=row[3],
                    pubDate=row[4],
                    source=row[5],
                )
                articles.append(article)
    return articles

def create_favorite_table(config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            link TEXT NOT NULL UNIQUE,
            pubDate TIMESTAMP,
            created TIMESTAMP,
            source TEXT
            )
            """)

def add_favorite_article(article,config):
    title = article.title
    description = article.description
    link = article.link
    pubDate = article.pubDate
    created = datetime.datetime.now()
    source = article.source
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO favorites (title, description, link, pubDate, created, source) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING""",(title, description, link, pubDate, created, source))

def get_favorite_articles(page,limit,config):
    offset = (page - 1) * limit
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            select id, title, description, link, pubDate, created, source
            from favorites
            ORDER BY created DESC
            LIMIT %s OFFSET %s
            """, (limit, offset))
            rows = cursor.fetchall()
            favorites = []
            for row in rows:
                favorite = Favorite(
                    id = row[0],
                    title=row[1],
                    description=row[2],
                    link=row[3],
                    pubDate=row[4],
                    created=row[5],
                    source=row[6],
                )
                favorites.append(favorite)
    return favorites

def get_favorite_article_by_id(article_id,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            select id, title, description, link, pubDate, created, source
            from favorites
            WHERE id = %s
            """, (article_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            article = Favorite(
                id=row[0],
                title=row[1],
                description=row[2],
                link=row[3],
                pubDate=row[4],
                created=row[5],
                source=row[6],
                )

    return article

def search_favorite_article(query,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""select id, title, description, link, pubDate, created, source from favorites
            WHERE title ILIKE %s OR description ILIKE %s""", (f'%{query}%',f'%{query}%'))
            rows = cursor.fetchall()
            favorites = []
            for row in rows:
                favorite = Favorite(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    link=row[3],
                    pubDate=row[4],
                    created=row[5],
                    source=row[6],
                )
                favorites.append(favorite)
    return favorites

def get_favorite_count(config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""select count(*) from favorites""")
            count = cursor.fetchone()[0]
    return count

def delete_article_from_favorites(id,config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM favorites WHERE id = %s""", (id,))


def clean_favorites(config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""Truncate favorites""")

def clean_articles(config):
    with get_connection(config) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""TRUNCATE articles""")

