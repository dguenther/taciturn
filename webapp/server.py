#!/usr/bin/python

from flask import Flask, render_template, session, g, request, redirect, url_for
import pymongo

DATABASE = {'host':'localhost', 'port':27017}
DEBUG = True
UPLOAD_FOLDER = '/tmp'
SECRET_KEY = '\x16C\xae+\xc99\xb4\x8d\xc7{\x8ex\x88\x1b8\x87\xd3\xe0L$VlOA'

# ADD ENSURE_INDEX

app = Flask(__name__)
app.config.from_object(__name__)

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

# NOT CONCURRENCY SAFE
# replace these with redis/memcached calls? or use just relational database
def get_campaign_id(db):
    c = list(db.units.find().sort('campaign_id', pymongo.DESCENDING).limit(0))
    if c:
        return c[0]['campaign_id'] + 1
def get_battle_id(db):
    b = list(db.units.find().sort('battle_id', pymongo.DESCENDING).limit(0))
    if b:
        return b[0]['battle_id'] + 1
    return 1
def get_unit_id(db):
    u = list(db.units.find().sort('unit_id', pymongo.DESCENDING).limit(0))
    if u:
        return u[0]['unit_id'] + 1
    return 1

@app.route('/')
def index():
    campaigns = g.db.users.find_one({'user_id': 1})['campaigns']
    # why are these becoming floats?
    campaigns = [int(c) for c in campaigns]
    print 'campaigns', campaigns
    return render_template('index.html', campaigns=campaigns)

@app.route('/setup')
@app.route('/setup/<int:campaign_id>')
def battle_setup(campaign_id=None):
    if campaign_id is None:
        campaign_id = get_campaign_id(g.db)
    battle_id = get_battle_id(g.db)
    units = g.db.units.find({'campaign_id': campaign_id})
    return render_template('battle_setup.html', units=units, campaign_id=campaign_id, battle_id=battle_id)

@app.route('/upload_units')
def upload_units():
    pass

@app.route('/edit_unit/<int:campaign_id>/<int:battle_id>')
@app.route('/edit_unit/<int:campaign_id>/<int:battle_id>/<int:unit_id>')
def edit_unit(campaign_id, battle_id, unit_id=None):
    # make new unit
    if unit_id is None:
        unit_id = get_unit_id(g.db)
        g.db.units.insert({'unit_id': unit_id, 'battle_id': battle_id, 'campaign_id': campaign_id})
    unit = g.db.units.find_one({'unit_id': unit_id})
    assert unit['campaign_id'] == campaign_id
    assert unit['battle_id'] == battle_id
    return render_template('edit_unit.html', unit=unit)

@app.route('/edit_unit', methods=['POST'])
def edit_unit_post():
    unit_id = int(request.form['unit_id'])
    unit = g.db.units.find_one({'unit_id': unit_id})
    unit['name'] = request.form['name']
    g.db.units.update({'unit_id': unit_id}, unit)
    return redirect(url_for(('battle_setup'), campaign_id=unit['campaign_id']))

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

if __name__ == '__main__':
    app.run()
