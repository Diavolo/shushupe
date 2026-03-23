# Shushupe

A free and open source blogging platform built with Python and [Django](https://www.djangoproject.com/).

It ships with apps for notes, reviews, bookmarks, and a changelog; a REST API documented with OpenAPI; and a front end using Tailwind CSS v4, Alpine.js, and assets built with Gulp.

- **Project site:** https://gahd.net/shushupe/
- **Live demo:** https://gahd.net
- **License:** MIT

## Requirements

- Python **3.12+** — with [pyenv](https://github.com/pyenv/pyenv), install a 3.12.x build and select it for this directory (for example via `.python-version`) before `poetry install`
- [Poetry](https://python-poetry.org/) for Python dependencies
- **Node.js** and npm to compile CSS/JS (Gulp and the Tailwind CLI)
- **PostgreSQL** (settings come from environment variables; SQLite is not the default)

## Installation

From the project root:

```sh
poetry install
npm install
```

Activate the virtual environment for this project so `python` points at the interpreter that has Django and the other dependencies installed. For example:

- **pyenv with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv):** `pyenv activate shushupe` (use the name of your env if it differs).
- **Poetry only:** `poetry shell` (activates the venv Poetry created for this project).

The rest of this document uses `python manage.py …`. If you skip activating a shell, use `poetry run python manage.py …` for the same commands.

## Configuration

1. **Environment variables:** copy `.env.sample` to `.env` and set data paths and database credentials.

2. **Secrets and site metadata:** copy `config.sample.json` to `config.json` in the project root and review at least `secret_key`, `site_name`, `site_url`, and `time_zone`. For production, also set `allowed_hosts` and `sentry` as expected by `shushupe/settings/prod.py`.

`SHUSHUPE_DATA_DIR` (optional in `.env`) controls where collected `media/` and `static/` live if you do not use the default paths.

## Database

Create the database and user in PostgreSQL to match your `.env`, then:

```sh
python manage.py migrate --settings=shushupe.settings.dev
```

To use the Django admin:

```sh
python manage.py createsuperuser --settings=shushupe.settings.dev
```

## Front-end assets (CSS/JS)

To rebuild styles and assets managed by npm/Gulp:

```sh
npm run build:dev    # development
npm run build:prod   # minified CSS for production
```

During development you can watch Tailwind with `npm run tailwindcss:watch`.

## Run (development)

```sh
python manage.py runserver --settings=shushupe.settings.dev
```

This settings module enables **Django Debug Toolbar** locally. Deploy with `shushupe.settings.prod` (for example via `gunicorn` and your environment variables).

## API and documentation

With the server running (and authentication where required):

- OpenAPI schema: `/api/schema/`
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

API routes are under `/api/`.
