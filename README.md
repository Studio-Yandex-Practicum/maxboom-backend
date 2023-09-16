# maxboom-backend
Интернет-магазин на DRF

Версия Python: 3.9
<br>Версия Django: 3.2.3

### Запуск текущей версии сервера на локальной машине
<br>— установить виртуальное окружение:
<br>```python -m venv venv```
— перейти в директорию ```maxboom_backend```
<br>```cd maxboom_backend```
<br>— установить зависимости окружения:
<br>```pip install -r requirements.txt```
<br>— настроить переменные окружения в соответствии с файлом ```.env.example```;
<br>— применить миграции:
<br>```python manage.py migrate```


### Запуск текущей версии контейнеров
<br>— настроить переменные окружения и базу данных в ```settings.py```;
<br>— сбилдить образы в docker-compose:
<br>```docker compose build```
<br>— запустить образы:
<br>```docker compose up```
<br>— применить миграции в контейнере backend:
<br>```docker compose exec backend python manage.py migrate```
<br>— собрать статику:
<br>```docker compose exec backend python manage.py collectstatic```
<br>— скопировать статику:
<br>```docker compose exec backend cp -r /app/collected_static/. /backend_static/static/```