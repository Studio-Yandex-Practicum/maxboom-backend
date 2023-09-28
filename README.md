## maxboom-backend

Интернет-магазин на DRF

Стек:
* Python 3.9
* Django 3.2.3

### Запуск текущей версии сервера на локальной машине
* установить виртуальное окружение:
```bash
python -m venv venv
```
* перейти в директорию ```maxboom_backend```
```bash
cd maxboom_backend
```
* установить зависимости окружения:
```bash
pip install -r requirements.txt
```
* настроить переменные окружения в соответствии с файлом ```.env.example```;
* применить миграции:
```bash
python manage.py migrate
```

### Запуск текущей версии контейнеров
<details>
<summary>С PostgreSQL</summary>

* настроить переменные окружения и базу данных в ```settings.py``` (установить database engine на postgresql);
* сбилдить образы в docker-compose:
```bash
docker compose -f docker-compose build
```
* запустить образы:
```bash
docker compose -f docker-compose up
```
* применить миграции в контейнере backend:
```bash
docker compose -f docker-compose exec backend python manage.py migrate
```
* собрать статику:
```bash
docker compose -f docker-compose exec backend python manage.py collectstatic
```
* скопировать статику:
```bash
docker compose -f docker-compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
</details>

<details>
<summary>С SQLite</summary>

* настроить переменные окружения и базу данных в ```settings.py``` (установить database engine на sqlite3);
* сбилдить образы в docker-compose:
```bash
docker compose -f docker-compose-sqlite build
```
* применить миграции в контейнере backend:
```bash
docker compose -f docker-compose-sqlite exec backend python manage.py migrate
```
* собрать статику:
```bash
docker compose -f docker-compose-sqlite exec backend python manage.py collectstatic
```
* скопировать статику:
```bash
docker compose -f docker-compose-sqlite exec backend cp -r /app/collected_static/. /backend_static/static/
```
</details>