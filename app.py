# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
#import sqlite3
import requests
from bs4 import BeautifulSoup
import re

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
from json import loads

import string

import ast
#ast.literal_eval("{'x':1, 'y':2}")

# create the application object
app = Flask(__name__)

# config
#app.secret_key = 'my precious'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

import os
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create the sqlalchemy object
db = SQLAlchemy(app)

# import db schema
from models import *


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    # return "Hello, World!"  # return a string
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)  # render a template


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/linklist', methods=['GET', 'POST', 'HEAD'])
def linklist():
    errors = []
    results = {}
    #http://www.indeed.ch/Stellen?q=sql&l=zurich&start=0

    if request.method == "POST":
        # get url that the user has entered

        for j in range(0,21,10):

            try:
                url = 'http://www.indeed.ch/Stellen?q=' + request.form['url'] + '&l=zurich&start=' + str(j)
                r = requests.get(url)
                soup = BeautifulSoup(r.content)
                script_soup = soup.find('script', text=re.compile('jobmap')).string # Which in this case is a dict within string so,
                #jobmap_regexp = 'jobmap\[3\]= ({.*?});'

                for i in range(0,10):
                    regexp_str = 'jobmap\[' + str(i) + '\]= ({.*?});'
                    codej = getJobmap(regexp_str,script_soup)

            except ValueError as err:
                errors.append(
                    "Unable to get URL. Please make sure it's valid and try again."
                )
                print(err)
    return render_template('linklist.html', errors=errors, results=results)

def getParams(url):
    params = url.split("&")[0]
    params = params.split('=')
    pairs = zip(params[0::1], params[1::1])
    answer = dict((k,v) for k,v in pairs)
    return answer

def getJobmap(jobmap_regexp,script_soup):
    jobmap = re.compile(jobmap_regexp, re.DOTALL)
    matches = jobmap.search(script_soup)
    code_raw = (matches.group(1))
    codej = code_raw.replace("jk", "'jk'")
    codej = codej.replace("efccid", "'efccid'")
    codej = codej.replace("srcid", "'srcid'")
    codej = codej.replace("cmpid", "'cxmpid'")
    codej = codej.replace("cmpesc", "'cxpesc'")
    codej = codej.replace("cmplnk", "'cxplnk'")
    codej = codej.replace("num", "'num'")
    codej = codej.replace("srcname", "'srcname'")
    codej = codej.replace("cmp", "'comp'")
    codej = codej.replace("locid", "'lxcid'")
    codej = codej.replace("loc", "'loc'")
    codej = codej.replace("country", "'country'")
    codej = codej.replace("zip", "'zip'")
    codej = codej.replace("city", "'city'")
    codej = codej.replace("title", "'title'")
    codej = codej.replace("rd", "'rd'")
    codej = codej.replace("\\", '#')
    codej = codej.replace("'", '"')
    codej = codej.replace("\\", "")
    codej = codej.replace("#", "\\")
    try:
        output_all = json.loads(codej)
        required_fields = ['jk', 'title', 'comp', 'loc']
        output = {key:value for key, value in output_all.items() if key in required_fields}
        json_obj = json.dumps(output)
        print('joblink: ', output['jk'], ', title: ', output['title'], ', company: ', output['comp'], ', location: ', output['loc'], )
        jstr = json.loads(json_obj)
        print(jstr)
    except ValueError as err:
        print(err)



@app.route('/browse', methods=['GET', 'POST'])
def browse():
    return render_template('browse.html')


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# connect to database
#def connect_db():
#    return sqlite3.connect('posts.db')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)