from news_parser.service.news_service import update_news
from news_parser.CLI.CLI import (
      get_user_choice, check_news_menu_choice, show_news_pages, show_sort_menu, get_sort_choice, show_source_menu,
      get_source_choice, show_date_menu, get_date_choice, show_found_news_pages, get_search_choice, show_favorite_menu,
      show_favorite_pages, check_range_menu, show_main_menu, show_news_menu, show_found_favorite_pages)
from news_parser.database.article_repository import create_main_table, create_favorite_table
from news_parser.service.article_service import get_articles_by_date_service, search_articles_service, clean_articles_service
from news_parser.service.favorite_service import search_favorite_article_service, clean_favorites_service
from config import Config


def main():

      config = Config()

      create_favorite_table(config)
      create_main_table(config)

      while True:
            show_main_menu()
            choice_main = get_user_choice()
            if check_range_menu(choice_main):
                  if choice_main == 1:
                        show_news_menu()
                        choice_user = get_user_choice()
                        if check_news_menu_choice(choice_user):
                              if choice_user == 1:
                                    show_news_pages(None,None,config)
                              elif choice_user == 2:
                                    show_sort_menu()
                                    sort = get_sort_choice()
                                    show_news_pages(None, sort,config)
                              elif choice_user == 3:
                                    show_source_menu()
                                    choice_source = get_source_choice()
                                    if choice_source == 1:
                                          show_news_pages("HackerNews", None,config)
                                    elif choice_source== 2:
                                          show_news_pages("Autosport F1", None,config)
                                    elif choice_source == 3:
                                          show_news_pages("BBC", None,config)
                              elif choice_user == 4:
                                    show_date_menu()
                                    choice = get_date_choice()
                                    articles = get_articles_by_date_service(choice,config)
                                    show_found_news_pages(articles,config)
                              elif choice_user == 5:
                                    print("Введите запрос: ")
                                    query = get_search_choice()
                                    articles = search_articles_service(query,config)
                                    show_found_news_pages(articles,config)
                  elif choice_main == 2:
                        show_favorite_menu()
                        choice_favorite = get_user_choice()
                        if choice_favorite == 1:
                              show_favorite_pages(config)
                        elif choice_favorite == 2:
                              print("Введите запрос: ")
                              query = get_search_choice()
                              favorites = search_favorite_article_service(query,config)
                              show_found_favorite_pages(favorites,config)
                        elif choice_favorite == 3:
                              clean_favorites_service(config)
                              print("Новостная лента очищена!")
                        elif choice_favorite == 4:
                              break
                  elif choice_main == 3:
                        update_news(config)
                        print("Новостная лента обновлена!")
                  elif choice_main == 4:
                        clean_articles_service(config)
                        print("Новостная лента очищена!")
                  elif choice_main == 5:
                        break

if __name__ == "__main__":
    main()