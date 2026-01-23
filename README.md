django_ecommerce1
=================

A typical eCommerce site built by django framework and Bootstrap 3

Run in django 5.2 and sqlite3

## Updates in 2026

### Current version

- Upgrade to Django 5.2 and Python 3.10
- Upgrade to the latest version of stripe
- Migrate database file to adapt modern Django framework
- Improve supporting documents
- Add a `.gitignore` file
- Optimize the URL patterns
- Restructure templates

## Installation

### Install with `uv` (recommended)

1. Install the prerequisites

```bash
uv sync
```

2. Update the database file

```bash
uv run manage.py migrate
```

3. *(Optional)* Create a superuser account

```bash
uv run manage.py createsuperuser
```

4. Collect static files (only for production deployment)

```bash
uv run manage.py collectstatic
```

5. Start the web service

```bash
uv run manage.py runserver
```

Press `Ctrl + C` to exit

### Install with `pip`

1. Establish a virtual environment

```bash
python3 -m venv venv
```

2. Activate the virtual environment

```bash
source venv/bin/activate
```

3. Install the prerequisites

```bash
python -m pip install -r requirements.in
```

4. Update the database file

```bash
python manage.py migrate
```

5. *(Optional)* Create a superuser account

```bash
python manage.py createsuperuser
```

6. Collect static files (only for production deployment)

```bash
python manage.py collectstatic
```

7. Start the web service

```bash
python manage.py runserver
```

Press `Ctrl + C` to exit

Run `deactivate` to leave the virtual environment

## Benchmark

```bash
python manage.py test
```


## Deprecated versions

Development records in Django 1.6 have been archived to the file `DEPRECATED.md`.
