#!/usr/bin/env python3
# Загрузка дерева каталога
# Файл должен лежать в папе проекта (рядом с manage.py)
import json
import os
from decimal import Decimal

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maxboom.settings')

# Initialize django application
try:
    django.setup()
    result = True
except Exception as e:
    print('Отказ запуска django', e)
    exit()

if result:
    import logging
    import time
    from http import HTTPStatus

    from catalogue.models import Product
    from catalogue.services.load_category_online import (APItokenAuth,
                                                         SaveHeadersSession,
                                                         is_valid)


def get_data_wb(path):
    auth = os.getenv('AUTHORIZATION')
    logging.info('Получен WB API token')
    if auth is False:
        logging.info('Необходимо добавить в .env WB API token'
                     '"AUTHORIZATION="')
        exit()
    headers = {
        'Content-Type': 'application/json'
    }
    url = ('https://suppliers-api.wildberries.ru/public/api/v1/info')
    i = 0
    s = SaveHeadersSession()
    while i < 3:
        i += 1
        try:
            response = s.get(url=url, headers=headers,
                             auth=APItokenAuth(auth), allow_redirects=True)
        except Exception as e:
            logging.info('Не получен список цен'
                         f' Ошибка: {e}')
        else:
            if response.status_code == HTTPStatus.OK:
                logging.info('Получен список цен')
                f_name = os.path.join(path, 'prices_online_wb.json')
                with open(f_name, 'w', encoding='utf-8') as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=2)
                return response.json()
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logging.info('Не получен список цен'
                             f' {response.status_code}')
                exit()
            else:
                logging.info('Не получен список цен'
                             f' {response.status_code}')
                time.sleep(1)
    exit()


def load_prices(path):
    # log_file = 'load_prices_online.log'
    # full_name = os.path.join(path, log_file)
    # logging.basicConfig(level=logging.INFO,
    #                     filename=full_name, filemode="w",
    #                     encoding='utf-8')
    # print(f'logfile: {log_file}')
    data = get_data_wb(path)
    update_db(data)


def update_db(data):
    for item in data:
        code = item.get('nmId')
        price = item.get('price')
        discount = item.get('discount')
        price = round(Decimal(price * (1 - discount / 100)), 2)

        if not Product.objects.filter(code=code).exists():
            logging.info(f'Нет товара с кодом: {code}')
        else:
            product = Product.objects.get(code=code)

            logging.info(
                f'Получен существующий товар: {product.name} {product.code}')
            if price != product.price:
                logging.info(
                    f'Заменена цена {product.price} на {price} '
                    f'для товара: {product.name} {product.code}'
                )
            product.price = price
            if is_valid(product):
                product.save()
                logging.info(
                    f'Обновлена цена товара: {product.name} {product.price}')


if __name__ == '__main__':
    load_prices()
