from flask import g, render_template, redirect, url_for, request, session, send_from_directory
import requests
import json
import os

from webapp import app, db
from webapp.utils import get_unit_id, get_battle_id, get_campaign_id
from webapp.models import Unit, Campaign, Battle, User

# TODO: authentication decorator
# http://flask.pocoo.org/docs/patterns/viewdecorators/
# http://flask.pocoo.org/snippets/8/
# or just pre-request handler that checks session.email?
# how to check if campaign/battle/unit user is trying to access belongs to them?

# TODO: make/find something to map form params to object fields (setattr)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# source: https://developer.mozilla.org/en-US/docs/Persona/Quick_Setup
@app.route('/auth/login', methods=['POST'])
def login():
    # The request has to have an assertion for us to verify
    if 'assertion' not in request.form:
        abort(400)
 
    # Send the assertion to Mozilla's verifier service.
    data = {'assertion': request.form['assertion'], 'audience': app.config['SERVER']['host']}
    resp = requests.post('https://verifier.login.persona.org/verify', data=data, verify=True)
 
    # Did the verifier respond?
    if resp.ok:
        # Parse the response
        verification_data = json.loads(resp.content)
 
        # Check if the assertion was valid
        if verification_data['status'] == 'okay':
            # Log the user in by setting a secure session cookie
            session.update({'email': verification_data['email']})
            # Check for user in database, make user if not found
            user = User.query.filter_by(email=session['email']).first()
            if user is None:
                user = User(email=session['email'])
                db.session.add(user)
                db.session.commit()
            # Add user_id to session
            session['user_id'] = user.id
            return resp.content
 
    # Oops, something failed. Abort.
    abort(500)

@app.route('/auth/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    print session
    if 'email' not in session:
        return render_template('index.html')

    user = User.query.filter_by(email=session['email']).first()
    assert user and user.campaigns is not None
    return render_template('index.html', campaigns=user.campaigns)

@app.route('/campaign/new', methods=['GET'])
def new_campaign():
    return render_template('campaign/new.html')
@app.route('/campaign/new', methods=['POST'])
def new_campaign_post():
    name = request.form['name']
    campaign = Campaign(name=name, user_id=session['user_id'])
    db.session.add(campaign)
    db.session.commit()
    return redirect(url_for('view_campaign', campaign_id=campaign.id))

@app.route('/campaign/edit/<int:campaign_id>', methods=['GET'])
def edit_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign/edit.html', campaign=campaign)
@app.route('/campaign/edit/<int:campaign_id>', methods=['POST'])
def edit_campaign_post(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.name = request.form['name']
    db.session.commit()
    return redirect(url_for('view_campaign', campaign_id=campaign.id))

@app.route('/campaign/<int:campaign_id>', methods=['GET'])
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign/view.html', campaign=campaign, units=campaign.units, battles=campaign.battles)

@app.route('/campaign/<int:campaign_id>/unit/new', methods=['GET'])
def new_unit(campaign_id):
    return render_template('unit/new.html')
@app.route('/campaign/<int:campaign_id>/unit/new', methods=['POST'])
def new_unit_post(campaign_id):
    unit = Unit(campaign_id=campaign_id)
    unit.name = request.form['name']
    unit.speed = request.form['speed']
    unit.ct = request.form['ct']
    unit.order_num = request.form['order_num']
    db.session.add(unit)
    db.session.commit()
    return redirect(url_for('view_campaign', campaign_id=campaign_id))

@app.route('/campaign/<int:campaign_id>/unit/edit/<int:unit_id>', methods=['GET'])
def edit_unit(campaign_id, unit_id):
    unit = Unit.query.get_or_404(unit_id)
    return render_template('unit/edit.html', unit=unit)
@app.route('/campaign/<int:campaign_id>/unit/edit/<int:unit_id>', methods=['POST'])
def edit_unit_post(campaign_id, unit_id):
    unit = Unit.query.get_or_404(unit_id)
    assert unit.campaign_id == campaign_id
    unit.name = request.form['name']
    unit.speed = request.form['speed']
    unit.ct = request.form['ct']
    db.session.commit()
    return redirect(url_for('view_campaign', campaign_id=campaign_id))


@app.route('/campaign/<int:campaign_id>/battle/new', methods=['GET'])
def new_battle(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('battle/new.html', units=campaign.units)
@app.route('/campaign/<int:campaign_id>/battle/new', methods=['POST'])
def new_battle_post(campaign_id):
    print request.form
    battle = Battle(campaign_id=campaign_id)
    battle.name = request.form['name']
    for unit_id in request.form.getlist('units'):
        unit = Unit.query.get(unit_id)
        battle.units.append(unit)
    db.session.add(battle)
    db.session.commit()
    return redirect(url_for('fight_battle', campaign_id=campaign_id, battle_id=battle.id))

@app.route('/campaign/<int:campaign_id>/battle/<int:battle_id>', methods=['GET'])
def fight_battle(campaign_id, battle_id):
    return "fight!"


