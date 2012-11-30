#!/usr/bin/python

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('webapp.cfg')
db = SQLAlchemy(app)
db.create_all()

import webapp.views
import webapp.models

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

