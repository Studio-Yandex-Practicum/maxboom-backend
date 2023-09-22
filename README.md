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

### Получение каталога категорий

GET <http://localhost:8000/api/catalogue/categories/>

```json
[
  {
    "id": 1,
    "name": "Автотовары",
    "slug": "avtotovaryi",
    "meta_title": null,
    "meta_description": null,
    "products": [],
    "branches": [
      {
        "id": 4,
        "name": "Автоэлектронника",
        "slug": "avtoelektronnika",
        "branches": [
          {
            "id": 2,
            "name": "FM-трансмиттеры",
            "slug": "fm-transmitteryi",
            "branches": []
          },
          {
            "id": 5,
            "name": "Автомобильные зарядные устройства",
            "slug": "avtomobilnyie-zaryadnyie-ustrojstva",
            "branches": []
          },
          {
            "id": 7,
            "name": "Сигнализации",
            "slug": "signalizatsii",
            "branches": []
          },
          {
            "id": 6,
            "name": "Сигнализации автомобильные",
            "slug": "signalizatsii-avtomobilnyie",
            "branches": []
          }
        ]
      }
    ],
    "root": null
  }
]
```

### Получение каталога категории по slug

GET <http://localhost:8000/api/catalogue/categories/fm-transmitteryi/>

```json
{
  "id": 2,
  "name": "FM-трансмиттеры",
  "slug": "fm-transmitteryi",
  "meta_title": null,
  "meta_description": null,
  "products": [
    {
      "id": 3,
      "category": "FM-трансмиттеры",
      "brand": "MaxBoom",
      "images": [
        {
          "image": "http://localhost:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_1.png",
          "thumbnail": "http://localhost:8000/media/cache/d7/40/d7400702f967b9543fb4399768b861fc.jpg"
        },
        {
          "image": "http://localhost:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_2.png",
          "thumbnail": "http://localhost:8000/media/cache/77/a8/77a80274c45287d13599cab559c6663f.jpg"
        },
        {
          "image": "http://localhost:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_4.png",
          "thumbnail": "http://localhost:8000/media/cache/42/9d/429d8612b6988f58d8b37dfbe1c31251.jpg"
        }
      ],
      "name": "Автомобильный переходник",
      "slug": "avtomobilnyij-perehodnik",
      "description": "Автомобильный FM трансмиттер для проигрывания музыки с USB флешки или через блютус со смартфона или ноутбука. Принцип работы простой: трансмиттер считывает аудио записи с различных носителей, а затем воспроизводит на настроенной частоте. Входящие звонки, при подключенном смартфоне, будут транслироваться на динамики автомобиля. У FM-трансмиттера присутствует функция Hands Free, которая позволяет свободно общаться по громкой связи. Данный трансмиттер имеет USB выход 5V 3.1A, благодаря которому всегда можно зарядить любой свой гаджет смартфон, планшет, наушники и пр. Прослушивание музыки с USB флешки. Встроенный плеер воспроизводит музыку в формате MP3 и WMA. Аксессуар работает от прикуривателя и оснащен тремя разъемами, LED-дисплеем, отображающим рабочую частоту или напряжение в сети, и кнопками для управления музыкой, вызовами и громкостью. Благодаря широкому диапазону напряжения FM-трансмиттер подходит для большинства марок автомобилей.",
      "price": "526.000",
      "code": 168978277,
      "wb_urls": "https://www.wildberries.ru/catalog/168978277/detail.aspx",
      "quantity": 999999.0,
      "is_deleted": false,
      "meta_title": null,
      "meta_description": null
    }
  ],
  "branches": [],
  "root": {
    "id": 4,
    "name": "Автоэлектронника",
    "slug": "avtoelektronnika",
    "root": {
      "id": 1,
      "name": "Автотовары",
      "slug": "avtotovaryi",
      "root": null
    }
  }
}
```

### Получение каталога по производителям

GET <http://localhost:8000/api/catalogue/brands/>

```json
[
  {
    "id": 1,
    "name": "MaxBoom",
    "slug": "maxboom",
    "products": [
      {
        "id": 3,
        "category": "FM-трансмиттеры",
        "brand": "MaxBoom",
        "images": [
          {
            "image": "http://127.0.0.1:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_1.png",
            "thumbnail": "http://127.0.0.1:8000/media/cache/d7/40/d7400702f967b9543fb4399768b861fc.jpg"
          },
          {
            "image": "http://127.0.0.1:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_2.png",
            "thumbnail": "http://127.0.0.1:8000/media/cache/77/a8/77a80274c45287d13599cab559c6663f.jpg"
          },
          {
            "image": "http://127.0.0.1:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_4.png",
            "thumbnail": "http://127.0.0.1:8000/media/cache/42/9d/429d8612b6988f58d8b37dfbe1c31251.jpg"
          }
        ],
        "name": "Автомобильный переходник",
        "slug": "avtomobilnyij-perehodnik",
        "description": "Автомобильный FM трансмиттер для проигрывания музыки с USB флешки или через блютус со смартфона или ноутбука. Принцип работы простой: трансмиттер считывает аудио записи с различных носителей, а затем воспроизводит на настроенной частоте. Входящие звонки, при подключенном смартфоне, будут транслироваться на динамики автомобиля. У FM-трансмиттера присутствует функция Hands Free, которая позволяет свободно общаться по громкой связи. Данный трансмиттер имеет USB выход 5V 3.1A, благодаря которому всегда можно зарядить любой свой гаджет смартфон, планшет, наушники и пр. Прослушивание музыки с USB флешки. Встроенный плеер воспроизводит музыку в формате MP3 и WMA. Аксессуар работает от прикуривателя и оснащен тремя разъемами, LED-дисплеем, отображающим рабочую частоту или напряжение в сети, и кнопками для управления музыкой, вызовами и громкостью. Благодаря широкому диапазону напряжения FM-трансмиттер подходит для большинства марок автомобилей.",
        "price": "526.000",
        "code": 168978277,
        "wb_urls": "https://www.wildberries.ru/catalog/168978277/detail.aspx",
        "quantity": 999999.0,
        "is_deleted": false,
        "meta_title": null,
        "meta_description": null
      }
    ]
  }
]

```

### Получение каталога товаров

GET <http://127.0.0.1:8000/api/catalogue/products/>

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "category": {
        "id": 2,
        "name": "FM-трансмиттеры",
        "slug": "fm-transmitteryi",
        "root": {
          "id": 4,
          "name": "Автоэлектронника",
          "slug": "avtoelektronnika",
          "root": {
            "id": 1,
            "name": "Автотовары",
            "slug": "avtotovaryi",
            "root": null
          }
        }
      },
      "brand": "MaxBoom",
      "images": [
        {
          "image": "http://127.0.0.1:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_1.png",
          "thumbnail": "http://127.0.0.1:8000/media/cache/d7/40/d7400702f967b9543fb4399768b861fc.jpg"
        },
        {
          "image": "http://127.0.0.1:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_2.png",
          "thumbnail": "http://127.0.0.1:8000/media/cache/77/a8/77a80274c45287d13599cab559c6663f.jpg"
        },
        {
          "image": "http://127.0.0.1:8000/media/products-images/%D0%91%D0%B5%D0%B7_%D0%BD%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F_4.png",
          "thumbnail": "http://127.0.0.1:8000/media/cache/42/9d/429d8612b6988f58d8b37dfbe1c31251.jpg"
        }
      ],
      "name": "Автомобильный переходник",
      "slug": "avtomobilnyij-perehodnik",
      "description": "Автомобильный FM трансмиттер для проигрывания музыки с USB флешки или через блютус со смартфона или ноутбука. Принцип работы простой: трансмиттер считывает аудио записи с различных носителей, а затем воспроизводит на настроенной частоте. Входящие звонки, при подключенном смартфоне, будут транслироваться на динамики автомобиля. У FM-трансмиттера присутствует функция Hands Free, которая позволяет свободно общаться по громкой связи. Данный трансмиттер имеет USB выход 5V 3.1A, благодаря которому всегда можно зарядить любой свой гаджет смартфон, планшет, наушники и пр. Прослушивание музыки с USB флешки. Встроенный плеер воспроизводит музыку в формате MP3 и WMA. Аксессуар работает от прикуривателя и оснащен тремя разъемами, LED-дисплеем, отображающим рабочую частоту или напряжение в сети, и кнопками для управления музыкой, вызовами и громкостью. Благодаря широкому диапазону напряжения FM-трансмиттер подходит для большинства марок автомобилей.",
      "price": "526.000",
      "code": 168978277,
      "wb_urls": "https://www.wildberries.ru/catalog/168978277/detail.aspx",
      "quantity": 999999.0,
      "is_deleted": false,
      "meta_title": null,
      "meta_description": null
    }
  ]
}
```