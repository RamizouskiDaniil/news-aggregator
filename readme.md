# News Aggregator

> Консольный агрегатор новостей на Python с RSS/XML-парсингом и PostgreSQL.

Приложение получает новости из RSS-источников, разбирает их, сохраняет в PostgreSQL и предоставляет консольный интерфейс для просмотра, поиска, сортировки и работы с избранным.

---

## Возможности

- Получение новостей из RSS-источников
- Парсинг RSS/XML
- Сохранение новостей в PostgreSQL
- Защита от дубликатов по `link`
- Просмотр новостей с пагинацией
- Сортировка новостей
- Фильтрация по источнику
- Фильтрация по дате
- Поиск по новостям
- Добавление новостей в избранное
- Просмотр и поиск избранных новостей
- Удаление избранных новостей
- Очистка новостной ленты
- Логирование ошибок
- Конфигурация через `.env`
- Unit- и integration-тесты

---

## Технологии

| Технология | Назначение |
|---|---|
| **Python** | Основной язык проекта |
| **PostgreSQL** | Хранение новостей и избранного |
| **psycopg** | Работа с PostgreSQL |
| **requests** | HTTP-запросы |
| **python-dotenv** | Загрузка конфигурации из `.env` |
| **pytest** | Тестирование |
| **XML / RSS** | Получение и обработка новостей |
| **Git** | Контроль версий |

---

## Архитектура

Проект разделён на несколько слоёв:

```text
CLI
 ↓
Service
 ↓
Repository
 ↓
PostgreSQL
```

Поток получения новостей:

```text
RSS
 ↓
Parser
 ↓
Service
 ↓
Repository
 ↓
PostgreSQL
```

### Основные директории

#### `CLI/`

Отвечает за взаимодействие с пользователем через консоль.

#### `service/`

Содержит логику взаимодействия между интерфейсом, парсером и repository.

#### `database/`

Отвечает за работу с PostgreSQL и SQL-запросы.

#### `parsers/`

Получает и разбирает RSS/XML.

#### `models/`

Содержит модели `Article` и `Favorite`.

#### `tests/`

Содержит unit- и integration-тесты.

---

## Структура проекта

```text
news_parser/
├── CLI/
│   ├── CLI.py
│   └── __init__.py
│
├── database/
│   ├── article_repository.py
│   ├── connection.py
│   └── __init__.py
│
├── models/
│   ├── models.py
│   └── __init__.py
│
├── parsers/
│   ├── XML_parser.py
│   └── __init__.py
│
├── service/
│   ├── article_service.py
│   ├── favorite_service.py
│   ├── news_service.py
│   └── __init__.py
│
├── tests/
│   ├── test_article_service.py
│   ├── test_parser.py
│   └── __init__.py
│
├── RSS/
│   └── rss_sourses.txt
│
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Установка

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd news_parser
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

### 3. Активация виртуального окружения

Для Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

---

## Настройка PostgreSQL

Создайте базу данных PostgreSQL.

После этого создайте файл `.env` в корне проекта:

```env
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

Заполните переменные своими данными PostgreSQL.

> `.env` не должен добавляться в Git.

Шаблон конфигурации находится в:

```text
.env.example
```

---

## Запуск

Запустите приложение:

```bash
python main.py
```

При запуске приложение создаёт необходимые таблицы и открывает консольное меню.

---

## Тестирование

Для запуска тестов:

```bash
python -m pytest -v
```

В проекте используются два типа тестов.

### Unit-тесты

Unit-тесты используются для изолированной проверки отдельных компонентов и логики приложения.

В проекте применяются:

- `pytest`
- fixtures
- `assert`
- `caplog`
- `monkeypatch`
- fake-зависимости

### Integration-тесты

Integration-тесты используются для проверки взаимодействия repository с PostgreSQL.

В частности, проверяется:

- добавление статьи в базу данных;
- защита от дубликатов по `link`.

---

## Логирование

Логи приложения записываются в:

```text
news_parser.log
```

Файл лога не должен попадать в Git.

---

## RSS-источники

RSS-источники хранятся в:

```text
RSS/rss_sourses.txt
```

Каждый источник содержит название и URL RSS-ленты.

---

## Конфигурация

Конфигурация приложения загружается из `.env`.

Используются следующие параметры:

```env
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

При отсутствии необходимой переменной конфигурации приложение вызывает `ConfigurationError`.

---

## Примечание

Проект создан как учебный backend-проект для практики:

- Python
- PostgreSQL
- архитектуры слоёв
- работы с API/RSS
- обработки ошибок
- логирования
- конфигурации
- тестирования

---