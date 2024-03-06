import datetime
import json
import logging
import os
import tempfile
import time
from http import HTTPStatus

import requests
from django.core import files
from django.core.exceptions import ValidationError
from requests.auth import AuthBase

from catalogue.models import Brand, Category, Product, ProductImage
from catalogue.services.load_category_online import load_categories
from catalogue.services.load_prices_online import load_prices
from maxboom.settings import MEDIA_ROOT, WB_API


class SaveHeadersSession(requests.Session):
    def rebuild_auth(self, prepared_request, response):
        pass


class APItokenAuth(AuthBase):
    """Attaches HTTP APItoken Authentication to the given Request object."""

    def __init__(self, username):
        self.username = username

    def __call__(self, r):
        r.headers['Authorization'] = self.username
        return r


def is_valid(obj):
    answer = True
    try:
        obj.full_clean()
    except ValidationError:
        logging.error(f'{type(obj)}, {obj.name}', exc_info=True)
        answer = False
    return answer


def card_data(s, url, headers, auth, nm_id=None, updated_at=None):
    query_data = {
        "sort": {
            "cursor": {
                "updatedAt": updated_at,
                "nmID": nm_id,
                "limit": 1000
            },
            "filter": {
                "withPhoto": -1
            }
        }
    }
    if nm_id is None:
        query_data.get('sort').get('cursor').pop('nmID')
    if updated_at is None:
        query_data.get('sort').get('cursor').pop('updatedAt')
    i = 0
    while i < 3:
        i += 1
        try:
            response = s.post(
                url=url, data=json.dumps(query_data), headers=headers,
                auth=APItokenAuth(auth), allow_redirects=True
            )
        except Exception as e:
            logging.info('Не получен список номенклатур товара'
                         f' Ошибка: {e}')
        else:
            if response.status_code == HTTPStatus.OK:
                logging.info('Получен список номенклатур товара')
                data = response.json().get('data')
                if data.get('cursor').get('total') >= 1000:
                    nm_id = data.get('cursor').get('nmID')
                    updated_at = data.get('cursor').get('updatedAt')
                    temp = card_data(
                        s, url, headers, auth, nm_id, updated_at
                    )
                    data['cards'] = data.get('cards') + temp.get('cards')
                return data
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logging.info('Не получен список номенклатур товара'
                             f' {response.status_code}')
                exit()
            logging.info('Не получен список номенклатур товара'
                         f' {response.status_code}')
            time.sleep(1)
    logging.info('Превышено количество попыток получить номенклатуры товара')
    exit()


def get_full_cards(s, headers, auth, vendor_code_part):
    query_data = {
        'vendorCodes': vendor_code_part,
        "allowedCategoriesOnly": False
    }
    url = 'https://suppliers-api.wildberries.ru/content/v1/cards/filter'
    i = 0
    while i < 3:
        i += 1
        try:
            response = s.post(
                url=url, data=json.dumps(query_data), headers=headers,
                auth=APItokenAuth(auth), allow_redirects=True
            )
        except Exception as e:
            logging.info('Не получен список с характеристиками'
                         f' Ошибка: {e}')
        else:
            if response.status_code == HTTPStatus.OK:
                logging.info('Получен список с характеристиками')
                return response.json().get('data')
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logging.info('Не получен список с характеристиками'
                             f' {response.status_code}')
                exit()
            else:
                logging.info('Не получен список с характеристиками'
                             f' {response.status_code}')
                time.sleep(1)
    logging.info('Превышено количество попыток получить характеристики товара')
    exit()


def get_data_wb(path):
    auth = WB_API
    logging.info(f'Получен WB API token {auth}')
    if auth is False:
        logging.info('Необходимо добавить в .env WB API token'
                     '"AUTHORIZATION="')
        exit()
    headers = {
        'Content-Type': 'application/json'
    }
    url = ('https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list')
    s = SaveHeadersSession()
    data = card_data(s, url, headers, auth)
    cards = data.get('cards')[:22]
    # cards = data.get('cards')
    f_name = os.path.join(path, 'cards_nm_online_wb.json')
    with open(f_name, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    cards_with_description = []
    # for i in range(0, len(cards), 5):
    for i in range(0, len(cards), 100):
        vendor_code_part = []
        # finish = i + 5
        finish = i + 100
        if finish > len(cards):
            finish = len(cards)
        for j in range(i, finish):
            vendor_code_part.append(cards[j].get('vendorCode'))
        cards_with_description += get_full_cards(
            s, headers, auth, vendor_code_part)
        # time.sleep(1)
    name = 'cards_full_online_wb.json'
    save_cards(cards=cards_with_description, path=path, name=name)
    return cards_with_description


def save_cards(cards, path, name):
    full_filename = os.path.join(path, name)
    with open(full_filename, 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)


def update_db(data):
    for item in data:
        category_name = item.get('object')
        wb_category_id = item.get('objectID')
        if not Category.objects.filter(name=category_name).exists():
            category = Category()
            category.name = category_name
            category.wb_category_id = wb_category_id
            if is_valid(category):
                category.save()
                logging.info(f'Создана категория: {category.name}')
            else:
                category = None
                logging.info(f'Не создана категория: {category.name}'
                             'Данные не прошли валидацию ')
        else:
            category = Category.objects.get(name=category_name)
            logging.info(
                'Получена существующая '
                f'категория: {category.name}'
            )
        price = item.get('sizes')[0].get('price')
        for characteristic in item.get('characteristics'):
            for key, value in characteristic.items():
                if key == 'Бренд':
                    brand = value
                    if not Brand.objects.filter(name=value).exists():
                        brand = Brand()
                        brand.name = value
                        if is_valid(brand):
                            brand.save()
                            logging.info(f'Создан производитель: {brand.name}')
                        else:
                            brand = None
                            logging.info(
                                f'Не создан производитель: {brand.name}'
                                'Данные не прошли валидацию '
                            )
                    else:
                        brand = Brand.objects.get(name=brand)
                        logging.info(
                            f'Получен существующий производитель: {brand.name}'
                        )
                    continue
                if key == 'Наименование':
                    product_name = value
                    continue
                if key == 'Описание':
                    product_description = value
        code = item.get('nmID')
        wb_urls = f'https://www.wildberries.ru/catalog/{code}/detail.aspx'
        vendor_code = item.get('vendorCode')
        imt_id = item.get('imtID')
        is_prohibited = item.get('isProhibited')
        if not Product.objects.filter(code=code).exists():
            product = Product()
            product.name = product_name
            product.price = price
            product.category = category
            product.brand = brand
            product.code = code
            product.description = product_description
            product.wb_urls = wb_urls
            product.imt_id = imt_id
            product.vendor_code = vendor_code
            product.is_deleted = is_prohibited
            if is_valid(product):
                product.save()
                logging.info(f'Создан товар: {product.name} {product.code}')
                for image_url in item.get('mediaFiles'):
                    add_image(image_url, product=product)

            else:
                product = None
                logging.info(f'Не создан товар: {product.name} {product.code}'
                             'Данные не прошли валидацию')
        else:
            product = Product.objects.get(code=code)
            logging.info(
                f'Получен существующий товар: {product.name} {product.code}')
            product.name = product_name
            product.price = price
            if product.category is None:
                product.category = category
                logging.info(
                    f'Добавлена категория {category} товару: {product.name}'
                    f' {product.code}'
                )
            if product.category != category:
                logging.info(
                    'Не совпала категория '
                    f'{product.category} != {category}'
                )
            product.brand = brand
            product.code = code
            product.description = product_description
            product.wb_urls = wb_urls
            product.imt_id = imt_id
            product.vendor_code = vendor_code
            product.is_deleted = is_prohibited
            if is_valid(product):
                product.save()
                logging.info(f'Обновлен товар: {product.name} {product.code}')
                for image_url in item.get('mediaFiles'):
                    add_image(image_url, product=product)
            else:
                product = None
                logging.info(f'Не обновлен товар: {product.name}'
                             f' {product.code}'
                             ' Данные не прошли валидацию')


def add_image(image_url, product):
    if product.images.all().exists():
        img_name = (
            '/'.join(product.images.all()[0].image.name.split(
                '/')[:-1]) + '/' + image_url.split('/')[-1]
        )
        if ProductImage.objects.filter(
            product=product, image=img_name
        ).exists():
            logging.info(
                f'Изображение "{img_name}" ранее'
                f' добавлено к товару "{product.name}"')
            return None

    # Stream the image from the url
    response = requests.get(image_url, stream=True)

    # Was the request OK?
    if response.status_code != requests.codes.ok:
        # Nope, error handling, skip file etc etc etc
        return
    # Get the filename from the url, used for saving later
    file_name = image_url.split('/')[-1]
    file_type = file_name.split('.')[-1]
    if file_type.upper() == 'MP4':
        return None
    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()
    # Read the streamed image in sections
    for block in response.iter_content(1024 * 8):
        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        lf.write(block)
    image = ProductImage()
    image.product = product
    image.image.save(file_name, files.File(lf))
    image.save()
    logging.info(
        f'Создано изображение "{image.image.name}" к товару "{product.name}"')
    # time.sleep(0.25)


def get_path():
    date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    if not os.path.exists(os.path.join(MEDIA_ROOT)):
        os.mkdir(os.path.join(MEDIA_ROOT))
    if not os.path.exists(os.path.join(MEDIA_ROOT, 'update')):
        os.mkdir(os.path.join(MEDIA_ROOT, 'update'))
    if not os.path.exists(os.path.join(MEDIA_ROOT, 'update', date)):
        os.mkdir(os.path.join(MEDIA_ROOT, 'update', date))
    if os.path.exists(os.path.join(MEDIA_ROOT, 'update', date)):
        return os.path.join(MEDIA_ROOT, 'update', date)
    exit()


def update_catalogue():
    log_file = 'load_catalogue.log'
    path = get_path()
    full_name = os.path.join(path, log_file)
    logging.basicConfig(level=logging.INFO,
                        filename=full_name, filemode="w",
                        encoding='utf-8')
    print(f'logfile: {full_name}')
    data = get_data_wb(path=path)
    update_db(data)
    load_categories(path)
    load_categories(path)
    load_prices(path)
    return True


if __name__ == '__main__':
    update_catalogue()
