#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import django
import logging


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maxboom.settings')
    try:
        django.setup()
    except Exception as e:
        print('Отказ запуска django', e)
        exit()
    else:
        logging.info("Успешно прошел запуск django")
    try:
        from catalogue.services.update_catalogue import (
            update_catalogue, get_path
        )
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    else:
        logging.info("Успешно импортирован update_catalogue, get_path")
    log_file = 'load_catalogue_script.log'
    path = get_path()
    full_name = os.path.join(path, log_file)
    logging.basicConfig(level=logging.INFO,
                        filename=full_name, filemode="w",
                        encoding='utf-8')
    print(f'logfile: {full_name}')
    update_catalogue()


if __name__ == '__main__':
    main()
