#!/usr /bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jiangge'

from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, render_template, redirect

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
db = SQLAlchemy(application)

class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    comment = db.Column(db.Text)
    url = db.Column(db.Text)
    create_at = db.Column(db.DateTime)
    
    def __init__(self, name, comment, url, create_at):
        self.name = name
        self.comment = comment
        self.url = url
        self.create_at = create_at

        
def save_data(name, comment, url, create_at):
    """
    save data from form submitted
    """
    db.session.add(posts(name, comment, url, create_at))
    db.session.commit()


def load_data(page):
    """
    load saved data
    """
    record_list = posts.query.all().pagenate(page, per_page=1, error_out=True)
    return record_list


@application.route('/', methods=['GET', 'POST'])
@application.route('/index/ ', methods=['GET', 'POST'])
@application.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page = 1):
    """Top page
    Use template to show the page
    """
    record_list = load_data(page)
    return render_template('index.html', record_list=record_list.items)


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
    db.create_all()
    application.run('0.0.0.0', port=80, debug=True)
