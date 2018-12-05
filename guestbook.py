#!/usr /bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jiangge'

import shelve
from datetime import datetime
from flask import Flask, request, render_template, redirect

application = Flask(__name__)

DATA_FILE = 'guestbook.dat'


def save_data(name, comment, url, create_at):
    """
    save data from form submitted
    """
    database = shelve.open(DATA_FILE)

    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']

    greeting_list.insert(
        0, {'name': name, 'comment': comment, 'url': url, 'create_at': create_at})

    database['greeting_list'] = greeting_list

    database.close()


def load_data(page):
    """
    load saved data
    """
    database = shelve.open(DATA_FILE)

    greeting_list = database.get('greeting_list', []).pagenate(page, per_page=1, error_out=True)

    database.close()

    return greeting_list


@application.route('/', methods=['GET', 'POST'])
@application.route('/index/ ', methods=['GET', 'POST'])
@application.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page = 1):
    """Top page
    Use template to show the page
    """
    greeting_list = load_data(page)
    return render_template('index.html', greeting_list=greeting_list.items)


@application.route('/post', methods=['POST'])
def post():
    """Comment's target url
    """
    name = request.form.get('name')
    comment = request.form.get('comment')
    url = request.form.get('url')
    create_at = datetime.now()

    save_data(name, comment, url, create_at)

    return redirect('/')


if __name__ == '__main__':
    application.run('0.0.0.0', port=80, debug=True)
