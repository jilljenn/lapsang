# Lapsang 山正

## Install

As we will import 7 million sentences from [Tatoeba](https://tatoeba.org/), it's better for you to use [PostgreSQL](https://www.postgresql.org).

This will install the Django development version, so that we can use the `ignore_conflicts` flag of `bulk_create` when importing the Tatoeba sentences.

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    ./manage.py migrate

Download Tatoeba's [sentences and links files](https://tatoeba.org/downloads), then:

    ./manage.py import --sentences /path/to/sentences.csv --links /path/to/links.csv # Should take 30 min
    ./manage.py runserver

Then you can access the routes `http://localhost:8000/sentences/eng` for example, or `http://localhost:8000/sentence/1`.
