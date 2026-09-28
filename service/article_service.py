from news_parser.database import article_repository

def get_article_service(article_id,config):
    return article_repository.get_article_by_id(article_id,config)

def get_articles_service(sourse,page, limit, sort,config):
    return article_repository.get_articles(sourse, page, limit, sort,config)

def get_articles_count_service(sourse,config):
    return article_repository.get_articles_count(sourse,config)

def get_articles_by_date_service(choice,config):
    return article_repository.get_articles_by_date(choice,config)

def search_articles_service(query,config):
    return article_repository.search_articles(query,config)

def add_article_service(article, config):
    article_repository.add_article(article,config)

def clean_articles_service(config):
    article_repository.clean_articles(config)

