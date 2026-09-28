import math
import webbrowser
from news_parser.service.article_service import get_article_service, get_articles_service,get_articles_count_service
from news_parser.service.favorite_service import add_favorite_article_service, get_favorite_count_service, get_favorite_articles_service, get_favorite_article_by_id_service, delete_article_from_favorite_service

def show_articles(articles):
    for article in articles:
        print(f'ID - {article.id}\n'
              f'Название - {article.title}\n'
              f'Описание - {article.description}\n'
              f'Ссылка - {article.link}\n'
              f'Дата публикации - {article.pubDate}\n'
              f'____________________________')



def show_news_pages(sourse, sort,config):
    limit = 10
    page = 1
    total_articles = get_articles_count_service(sourse,config)
    total_pages = math.ceil(total_articles / limit)
    while True:
        print(f'================================\n'
              f'Страница {page} из {total_pages}\n'
              f'================================')
        articles = get_articles_service(sourse, page, limit, sort,config)
        show_articles(articles)
        choice = input(f'R - выбрать новость \n'
                       f'Q - следующая страница\n'
                       f'W - предыдущая страница\n'
                       f'E - выйти\n')
        if choice == "r":
            id_choice = input(f'Введите ID новости: ')
            article = get_article_service(id_choice,config)
            show_chosen_article(article)
            while True:
                show_news_action_menu()
                action_choice = get_action_choice()
                if action_choice == 1:
                    webbrowser.open_new(article.link)
                elif action_choice == 2:
                    add_favorite_article_service(article,config)
                    print("Новость добавлена в избранное ")
                elif action_choice == 3:
                    break
        elif choice == "q":
            if page < total_pages:
                page += 1
            else:
                print(f'Вы находитесь на последней странице ')
        if choice == "w":
            if page > 1:
                page -= 1
            else:
                print("Вы находитесь на первой странице ")
        if choice == "e":
            break

def show_found_news_pages(articles,config):
    limit = 10
    page = 1
    total_articles = len(articles)
    total_pages = math.ceil(total_articles / limit)
    while True:
        print(f'================================\n'
              f'Страница {page} из {total_pages}\n'
              f'================================')
        offset = (page - 1) * limit
        show_articles(articles[offset:offset+limit])
        choice = input(f'R - выбрать новость \n'
                       f'Q - следующая страница\n'
                       f'W - предыдущая страница\n'
                       f'E - выйти')
        if choice == "r":
            id_choice = input(f'Введите ID новости: ')
            article = get_article_service(id_choice,config)
            show_chosen_article(article)
            while True:
                show_news_action_menu()
                action_choice = get_action_choice()
                if action_choice == 1:
                    webbrowser.open_new(article.link)
                elif action_choice == 2:
                    add_favorite_article_service(article,config)
                elif action_choice == 3:
                    break
        elif choice == "q":
            if page < total_pages:
                page += 1
            else:
                print(f'Вы находитесь на последней странице ')
        if choice == "w":
            if page > 1:
                page -= 1
            else:
                print("Вы находитесь на первой странице ")
        if choice == "e":
            break

def show_chosen_article(article):
    print(f'ID - {article.id}\n'
          f'Название - {article.title}\n'
          f'Описание - {article.description}\n'
          f'Ссылка - {article.link}\n'
          f'Дата публикации - {article.pubDate}\n')



def show_favorite_pages(config):
    limit = 10
    page = 1
    total_favorites = get_favorite_count_service(config)
    if total_favorites > 0:
        total_pages = math.ceil(total_favorites / limit)
        while True:
            print(f'================================\n'
                f'Страница {page} из {total_pages}\n'
                f'================================')
            favorites = get_favorite_articles_service(page,limit,config)
            show_articles(favorites)
            choice = input(f'R - выбрать новость\n'
                       f'Q - следующая страница\n'
                       f'W - предыдущая страница\n'
                       f'E - выйти\n')
            if choice == "r":
                id_choice = input('Введите ID новости: ')
                favorite = get_favorite_article_by_id_service(id_choice,config)
                show_chosen_favorite(favorite)
                while True:
                    show_favorite_action_menu()
                    action_choice = get_favorite_action_choice()
                    if action_choice == 1:
                        webbrowser.open_new(favorite.link)
                    elif action_choice == 2:
                        delete_article_from_favorite_service(id_choice,config)
                        print('Новость удалена из избранного ')
                    elif action_choice == 3:
                        break
            elif choice == "q":
                if page < total_pages:
                    page += 1
                else:
                    print(f'Вы находитесь на последней странице ')
            if choice == "w":
                if page > 1:
                    page -= 1
                else:
                    print("Вы находитесь на первой странице ")
            if choice == "e":
                break
    else:
        print('Избранное пусто ')
        return

def show_found_favorite_pages(favorites,config):
    limit = 10
    page = 1
    total_favorites = len(favorites)
    total_pages = math.ceil(total_favorites / limit)
    while True:
        print(f'================================\n'
              f'Страница {page} из {total_pages}\n'
              f'================================')
        offset = (page - 1) * limit
        show_articles(favorites[offset:offset + limit])
        choice = input(f'R - выбрать новость\n'
                       f'Q - следующая страница\n'
                       f'W - предыдущая страница\n'
                       f'E - выйти\n')
        if choice == "r":
            id_choice = input('Введите ID новости: ')
            favorite = get_favorite_article_by_id_service(id_choice,config)
            show_chosen_favorite(favorite)
            while True:
                show_favorite_action_menu()
                action_choice = get_favorite_action_choice()
                if action_choice == 1:
                    webbrowser.open_new(favorite.link)
                elif action_choice == 2:
                    delete_article_from_favorite_service(id_choice,config)
                    print('Новость удалена из избранного ')
                elif action_choice == 3:
                    break
        elif choice == "q":
            if page < total_pages:
                page += 1
            else:
                print(f'Вы находитесь на последней странице ')
        if choice == "w":
            if page > 1:
                page -= 1
            else:
                print("Вы находитесь на первой странице ")
        if choice == "e":
            break

def show_chosen_favorite(favorite):
    print(f'ID - {favorite.id}\n'
          f'Название - {favorite.title}\n'
          f'Описание - {favorite.description}\n'
          f'Ссылка - {favorite.link}\n'
          f'Дата публикации - {favorite.pubDate}\n')



def show_favorite_action_menu():
    print(f'1. Открыть ссылку \n'
          f'2. Удалить из избранного \n'
          f'3. Назад \n')

def show_favorite_menu():
    print(f'=== FAVORITES ===\n'
          f'1. Показать избранное \n'
          f'2. Поиск \n'
          f'3. Очистить \n'
          f'4. Назад \n')

def show_news_action_menu():
    print(f'=== Действия ===\n'
          f'1. Открыть ссылку\n'
          f'2. Добавить в избранное\n'
          f'3. Выйти \n')

def show_date_menu():
    print(f'=== FILTER BY DATE ===\n'
          f'\n'
          f'1. За сегодня \n'
          f'2. За последние 3 дня \n'
          f'3. За последнюю неделю \n'
          f'4. За последний месяц \n')

def show_sort_menu():
    print(f'1. Новые → старые \n'
          f'2. Старые → новые \n'
          f'3. Название A → Z \n'
          f'4. Название Z → A \n')

def show_main_menu():
    print(f'=== NEWS AGGREGATOR ===\n'
          f'1. Посмотреть новости \n'
          f'2. Избранное \n'
          f'3. Обновить \n'
          f'4. Очистить\n'
          f'5. Выйти')

def show_news_menu():
    print(f'=== NEWS SHOW MENU ===\n'
          f'1. Показать все новости \n'
          f'2. Сортировка \n'
          f'3. По источнику \n'
          f'4. По дате \n'
          f'5. Поиск \n')

def show_source_menu():
    print(f'=== SHOW NEWS ===\n'
          f'1. HackerNews \n'
          f'2. Formula 1 \n'
          f'3. BBC \n')



def get_favorite_action_choice():
    while True:
        try:
            choice = int(input())
            if 0 < choice <= 3:
                return choice
        except ValueError:
            print("Введите корректное значение: ")

def get_source_choice():
    while True:
        try:
            choice = int(input())
            if 0 < choice <= 3:
                return choice
        except ValueError:
            print("Введите корректное значение: ")

def get_action_choice():
    while True:
        try:
            choice = int(input())
            if 0 < choice <= 3:
                return choice
        except ValueError:
            print("Введите корректное значение: ")

def get_date_choice():
    while True:
        try:
            choice = int(input())
            if choice == 1:
                return "1 day"
            elif choice == 2:
                return "3 days"
            elif choice == 3:
                return "7 days"
            elif choice == 4:
                return "30 days"
        except ValueError:
            print(f'Введите корректное значение: ')

def get_user_choice():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Введите корректное значение ")

def get_search_choice():
    while True:
        choice = input().strip()
        if choice != "":
            return choice
        else:
            print("Введите корректный запрос: ")

def get_sort_choice():
    while True:
        try:
            a = int(input())
            if a == 1:
                return "pubDate DESC"
            elif a == 2:
                return "pubDate ASC"
            elif a == 3:
                return "title ASC"
            elif a == 4:
                return "title DESC"
            else:
                print(f'Введите корректное значение: ')
        except ValueError:
            print(f'Введите корректное значение: ')



def check_news_menu_choice(choice):
    return 0 < choice <= 5

def check_range_menu(choice):
    return 0 < choice <= 5

def check_news_menu(choice):
    return 0 < choice <= 5