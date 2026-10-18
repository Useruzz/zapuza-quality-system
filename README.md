# Zapuza Factory Operations & Quality Control System

A Python and Django web application for managing production jobs and quality inspections in a factory.

## Features

- Create and track production jobs.
- Monitor production job statuses.
- Record quality inspections for production jobs.
- Automatically calculate inspection results as PASS or FAIL using minimum and maximum acceptable values.
- View production and quality summaries on the factory dashboard.
- Manage records through Django Admin.
- Validate production workflows using automated tests.

## Technology Stack

- Python
- Django
- SQLite
- HTML
- Django Templates

## Setup Instructions

### 1. Clone or download the project

Open a terminal in the project directory.

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Django

```bash
pip install Django
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to configure the account.

### 6. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. If port 8000 is occupied, use `python manage.py runserver 8001`.

## Running Tests

Run all automated tests:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test production
python manage.py test quality
```

## Project Structure

- `config/` — Django project configuration.
- `production/` — Production job management.
- `quality/` — Quality inspection management.
- `dashboard/` — Factory dashboard and summaries.
- `templates/` — HTML templates.
- `manage.py` — Django management utility.

## Notes

The project uses SQLite by default. Database files and local environment files should not be committed to version control.

## Demonstration Video

[Watch the project demonstration](https://youtu.be/CNrDejv2XuI)
