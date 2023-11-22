#!/usr/bin/env python3
# Загрузка дерева каталога
# Файл должен лежать в папе проекта (рядом с manage.py)
import json
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'maxboom.settings')

# Initialize django application
try:
    django.setup()
except Exception as e:
    print('Отказ запуска django', e)
    exit()
else:
    import logging
    import time
    from http import HTTPStatus

    import requests
    from django.core.exceptions import ValidationError
    from dotenv import load_dotenv
    from requests.auth import AuthBase

    from catalogue.models import Category

    load_dotenv()


class SaveHeadersSession(requests.Session):
    def rebuild_auth(self, prepared_request, response):
        pass


class APItokenAuth(AuthBase):
    """Attaches HTTP APItoken Authentication to the given Request object."""

    def __init__(self, username):
        # setup any auth-related data here
        self.username = username

    def __call__(self, r):
        # modify and return the request
        r.headers['Authorization'] = self.username
        return r


def get_data_wb():
    auth = os.getenv('AUTHORIZATION')
    logging.info('Получен WB API token')
    if auth is False:
        logging.info('Необходимо добавить в .env WB API token'
                     '"AUTHORIZATION="')
        exit()
    headers = {
        'Content-Type': 'application/json'
    }
    url = ('https://suppliers-api.wildberries.ru/content/'
           'v1/object/all/?top=8000')
    i = 0
    s = SaveHeadersSession()
    while i < 3:
        i += 1
        try:
            response = s.get(url=url, headers=headers,
                             auth=APItokenAuth(auth), allow_redirects=True)
        except Exception as e:
            logging.info('Не получен список категорий'
                         f' Ошибка: {e}')
        else:
            if response.status_code == HTTPStatus.OK:
                logging.info('Получен список категорий')
                return response.json().get('data')
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logging.info('Не получен список категорий'
                             f' {response.status_code}')
                exit()
            logging.info('Не получен список категорий'
                         f' {response.status_code}')
            time.sleep(1)
    exit()


def load_categories(path):
    # log_file = 'load_category_online.log'
    # full_name = os.path.join(path, log_file)
    # logging.basicConfig(level=logging.INFO,
    #                     filename=full_name, filemode="w",
    #                     encoding='utf-8')
    # print(f'logfile: {log_file}')
    data = get_data_wb()
    f_name = os.path.join(path, 'category_full_online_wb.json')
    with open(f_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    update_category_db(data=data)


def update_category_db(data):
    for item in data:
        category_id = item.get('objectID')
        category_name = item.get('objectName')
        category_is_prohibited = not item.get('isVisible')
        if not Category.objects.filter(wb_category_id=category_id).exists():
            # category = Category()
            # category.name = category_name
            # category.wb_category_id = category_id
            # category.root = get_parent_category(item)
            # category.is_prohibited = category_is_prohibited
            logging.info(f'Не создана подкатегория: {category_name}'
                         ' Нет товаров в этой подкатегории')
        else:
            category = Category.objects.get(
                wb_category_id=category_id
            )
            category.name = category_name
            category.wb_category_id = category_id
            category.root = get_parent_category(item)
            category.is_prohibited = category_is_prohibited
            logging.info(f'Обновлена подкатегория: {category.name}')
            if is_valid(category):
                category.save()
            else:
                logging.info('Данные не прошли валидацию')
    return None


def get_parent_category(item):
    parent_id = item.get('parentID')
    parent_name = item.get('parentName')
    if not Category.objects.filter(wb_category_id=parent_id).exists():
        category_parent = Category()
        category_parent.name = parent_name
        category_parent.wb_category_id = parent_id
        if is_valid(category_parent):
            category_parent.save()
            logging.info(
                f'Создана родительская категория: {category_parent.name}')
        else:
            logging.info('Данные не прошли валидацию ')
            return None
    else:
        category_parent = Category.objects.get(
            wb_category_id=parent_id)
        logging.info(
            'Получена существующая родительская '
            f'категория: {category_parent.name}'
        )
    return category_parent


def is_valid(obj):
    answer = True
    try:
        obj.full_clean()
    except ValidationError:
        logging.error(f'{type(obj)}, {obj.name}', exc_info=True)
        answer = False
    return answer


if __name__ == '__main__':
    load_categories()
