# Блогикум

## О проекте

Социальная сеть для публикации личных дневников. Это будет сайт, на котором пользователь может создать свою страницу и публиковать на ней сообщения («посты»). Для каждого поста нужно указать категорию — например «путешествия», «кулинария» или «python-разработка», а также опционально локацию, с которой связан пост, например «Остров отчаянья» или «Караганда». Пользователь может перейти на страницу любой категории и увидеть все посты, которые к ней относятся. Пользователи смогут заходить на чужие страницы, читать и комментировать чужие посты. Добавлять картинки к постам.

## Автор проекта:
Валерий Шанкоренко<br/>
Github: [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram:[@valeron007](https://t.me/valeron007)<br/>
E-mail:valerashankorenko@yandex.by<br/>

## Стек технологий
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [SQLite](https://www.sqlite.org/)

## Как запустить проект:
1. Клонировать репозиторий и перейти в его директорию в командной строке:
```shell
git clone git@github.com:valerashankorenko/django_sprint4.git
```
2. Переход в директорию django_sprint4
```shell
cd django_sprint4
```
3. Создание виртуального окружения
```shell
python -m venv venv
```
4. Активация виртуального окружения
```shell
source venv/Scripts/activate
```
5. Обновите pip
```shell
python -m pip install --upgrade pip
```
6. Установка зависимостей
```shell
pip install -r requirements.txt
```
7. Применение миграций
```shell
python manage.py migrate
```
8. Загрузить фикстуры в БД
```shell
python manage.py loaddata db.json
```
9. Создать суперпользователя
```shell
python manage.py createsuperuser
```
10. Запуск проекта
```shell
python manage.py runserver
```
