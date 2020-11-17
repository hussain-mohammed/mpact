# mpact

A Telegram-based expert support system

## Installing a development environment

1. Install prerequisite packages

       $ sudo apt install python3.8-venv

2. Create and activate a Python virtual environment

       $ python3.8 -m venv venv
       $ source venv/bin/activate

3. Install requirements

       $ pip install -r requirements.txt

## Set Environment Variables

    $ export SECRET_KEY=<Django Secret Key>
    $ export TOKEN=<Telegram Bot Token>
    $ export BOT_USERNAME=<Telegram Bot Username>
    $ export ALLOWED_HOSTS='127.0.0.1 localhost'

## Run

    $ cd mpact_api
    $ ./manage.py runserver
