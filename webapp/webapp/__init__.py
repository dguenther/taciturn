#!/usr/bin/python

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
import pymongo

DATABASE = {'host':'localhost', 'port':27017}
DEBUG = True
UPLOAD_FOLDER = '/tmp'
SECRET_KEY = '\x16C\xae+\xc99\xb4\x8d\xc7{\x8ex\x88\x1b8\x87\xd3\xe0L$VlOA'
SQLALCHEMY_DATABASE_URI = 'sqllite:////tmp/test.db'

# ADD ENSURE_INDEX

app = Flask(__name__)
app.config.from_object(__name__)
#db = SQLAlchemy(app)

import webapp.views
import webapp.models

def connect_db():
    """Returns a new connection to the database."""
    return pymongo.Connection(**app.config['DATABASE'])['taciturn']

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.connection.close()

#def allowed_file(filename):
#    return '.xls' in filename
#
#@app.route('/upload_units', methods=['POST'])
#def upload_units():
#    file = request.files['file']
#    if file and allowed_file(file.filename):
#        filename = secure_filename(file.filename)
#        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#        return redirect(url_for('prebattle'))

