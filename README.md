# Bosco Backend

Навчальний складський застосунок на Django з каталогом товарів.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Головна сторінка показує каталог товарів, а форма `/products/new/` додає товар із CSRF-захистом.

## Структура

- `catalog/` — модель `Product`, форма, views, admin та template tags.
- `templates/` — базовий layout, сторінки каталогу та partials.
- `static/` — стилі застосунку.
