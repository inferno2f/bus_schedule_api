# NJ Transit - Bus schedule API

## Description
API service for quick and easy access to New Jersey's bus schedule. Data provided by [NJ Transit](https://www.njtransit.com).

## Prerequisites
- Python 3.9+
- PostgreSQL
- Developer account with [NJ Transit](https://www.njtransit.com/developer-tools) to obtain relevant GTFS data

## Quick start
Clone the repository from Github and switch to relevant folder:

    $ git clone git@github.com:inferno2f/bus_schedule_api.git
    $ cd path_to_folder/bus_schedule_api

Create virtual env and install requirements:

    $ python -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Create `.env` file and define necessary environment variables. Required variable are listed in `.env_example` file:
    
    $ touch .env

Migrate database (from the root folder of the project):

    $ python manage.py migrate

Launch local dev server:

    $ python manage.py runserver

## Populating database with GTFS data

Access and download most relevant GTFS data from NJ Transit website (developer tools section).

Add `static/` folder to the root folder of your project and copy `.txt` files with GTFS data there.

Run a built-in command to populate your database with GTFS data
    
    $ python manage.py gtfs_parser

### Author
Vlad Nikitin - [nikitinv91@gmail.com](mailto:nikitinv91@gmail.com)

### License
Standard MIT License
