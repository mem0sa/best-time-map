Best Time Map

Веб-сервис для поиска оптимального времени посещения различных локаций и организаций.
Проект помогает пользователям выбрать наиболее комфортный день недели и час для визита, анализируя предполагаемую загруженность и визуализируя результаты в виде наглядной таблицы.

Сервис ориентирован на тех, кто хочет избегать пиковых часов и планировать посещения более эффективно.

Ссылка на рабочий проект:
https://memoza.pythonanywhere.com

Технологии
Python 3.10
Django 5.x
HTML5 / CSS3
JavaScript (Vanilla JS)
Google Maps JavaScript API
Google Places API
SQLite (разработка)

Скриншоты

![Главная страница](screenshots/main_page.png)
Главная страница с интерактивной картой и возможностью выбора локации

![Главная страница](screenshots/visit_time_info.png)
Таблица загруженности по дням недели и часам с выделением оптимального времени посещения

Как запустить проект локально

Клонируйте репозиторий:
git clone https://github.com/ваш-юзернейм/best-visit-time-map.git

Перейдите в папку проекта:
cd best-visit-time-map

Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

Установите зависимости:
pip install -r requirements.txt

Выполните миграции базы данных:
python manage.py migrate

Запустите сервер разработки:
python manage.py runserver

Откройте проект в браузере:
Перейдите по адресу:
http://127.0.0.1:8000/