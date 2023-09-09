# maxboom-backend
Интернет-магазин на DRF

Версия Python: 3.9
<br>Версия Django: 3.2.3

### Запуск текущей версии на локальной машине
— установить виртуальное окружение:
<br>```python -m venv venv```
<br>— установить зависимости окружения:
<br>```pip install -r requirements.txt```
<br>— настроить переменные окружения в соответствии с файлом .env.example;
<br>— применить миграции:
<br>```python manage.py migrate```

### Получение отзывов о магазине

GET <http://localhost:8000/api/store-reviews/>

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "pk": 1,
      "text": "Интересный ассортимент в магазине.",
      "pub_date": "2023-09-09T05:16:46.271498Z",
      "author_name": "Федор Иванович",
      "author_email": null,
      "average_score": 3.0,
      "delivery_speed_score": 4,
      "quality_score": 3,
      "price_score": 2,
      "replay": {
        "text": "Работаем для вас.",
        "pub_date": "2023-09-09T05:17:42.651783Z",
        "name": "Администратор"
      }
    }
  ]
}
```