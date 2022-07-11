![Foodgram workflow](https://github.com/kh199/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# сайт Foodgram, «Продуктовый помощник»

Проект доступен по ссылке http://http://158.160.7.215/recipes

Aдминка:
логин: admin1
пароль: Admin12345

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка 

Клонировать репозиторий:

git clone https://github.com/kh199/foodgram-project-react.git

## Запуск на удаленном сервере:

Установите docker на удаленный сервер:
```
sudo apt install docker.io 

```
Скопируйте файлы docker-compose.yml и nginx.conf из папки infra на сервер

## Локально:

Создать и заполнить файл .env:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Отредактируйте файл nginx.conf: в строке server_name впишите свой ip

### Добавить в Github Secrets:

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DOCKER_PASSWORD= юзернейм для dockerhub
DOCKER_USERNAME= пароль для dockerhub
SECRET_KEY= секретный ключ django
USER= юзернейм для подключения к удаленному серверу
HOST= ваш ip
PASSPHRASE= пароль, если установлен
SSH_KEY= SSH ключ
TELEGRAM_TO= ваш id в телеграме
TELEGRAM_TOKEN= токен вашего бота 


### После деплоя на сервере:

Выполнить миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
Создать суперпользователя:
```
sudo docker-compose exec backend python manage.py createsuperuser
```
Подгрузить статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input 
```
Загрузить базу данных ингредиентов:
```
sudo docker-compose exec backend python manage.py load_ingredients
```

