from webapp import app
from flask import g, render_template, redirect, url_for, request
from webapp.utils import get_unit_id, get_battle_id, get_campaign_id

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

