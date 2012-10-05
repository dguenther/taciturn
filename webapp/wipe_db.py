#!/usr/bin/python

from webapp import db
db.drop_all()
db.create_all()
