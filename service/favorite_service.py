from news_parser.database import article_repository

def add_favorite_article_service(article,config):
    return article_repository.add_favorite_article(article,config)

def get_favorite_count_service(config):
    return article_repository.get_favorite_count(config)

def get_favorite_articles_service(page,limit,config):
    return article_repository.get_favorite_articles(page,limit,config)

def get_favorite_article_by_id_service(id,config):
    return article_repository.get_favorite_article_by_id(id,config)

def delete_article_from_favorite_service(id,config):
    return article_repository.delete_article_from_favorites(id,config)

def search_favorite_article_service(query,config):
    return article_repository.search_favorite_article(query,config)

def clean_favorites_service(config):
    return article_repository.clean_favorites(config)

