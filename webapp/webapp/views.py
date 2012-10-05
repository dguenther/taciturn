from flask import g, render_template, redirect, url_for, request, session
import requests
import json

from webapp import app, db
from webapp.utils import get_unit_id, get_battle_id, get_campaign_id
from webapp.models import Unit, Campaign, Battle, User

# authentication decorator
# http://flask.pocoo.org/docs/patterns/viewdecorators/
# http://flask.pocoo.org/snippets/8/
# or just pre-request handler that checks session.email?

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
    return redirect(url_for('index'))

@app.route('/')
def index():
    print session
    print session.get('email')
    print dir(session)
    if 'email' not in session:
        return render_template('index.html')

    user = User.query.filter_by(email=session['email']).first()
    assert user and user.campaigns is not None
    return render_template('index.html', campaigns=user.campaigns)

@app.route('/setup')
@app.route('/setup/<int:campaign_id>')
def battle_setup(campaign_id=None):
    if campaign_id is None:
        campaign = Campaign(user_id=session['user_id'])
        db.session.add(campaign)
        db.session.commit()
    else:
        campaign = Campaign.query.filter_by(id=campaign_id).first()
    battle = Battle(campaign_id=campaign.id)
    db.session.add(battle)
    db.session.commit()
    units = Unit.query.filter_by(campaign_id=campaign.id)
    return render_template('battle_setup.html', units=units, campaign_id=campaign.id, battle_id=battle.id)

@app.route('/upload_units')
def upload_units():
    pass

@app.route('/edit_unit/<int:campaign_id>/<int:battle_id>')
@app.route('/edit_unit/<int:campaign_id>/<int:battle_id>/<int:unit_id>')
def edit_unit(campaign_id, battle_id, unit_id=None):
    # make new unit
    battle = Battle.query.filter_by(id=battle_id).first()
    if unit_id is None:
        unit = Unit(campaign_id=campaign_id, battles=[battle])
        db.session.add(unit)
        db.session.commit()
    else:
        unit = Unit.query.filter_by(id=unit_id).first()
    assert unit.campaign_id == campaign_id
    assert any([x.id == battle_id for x in unit.battles])
    return render_template('edit_unit.html', unit=unit)

@app.route('/edit_unit', methods=['POST'])
def edit_unit_post():
    unit_id = int(request.form['unit_id'])
    unit = Unit.query.filter_by(id=unit_id).first()
    unit.name = request.form['name']
    db.session.commit()
    return redirect(url_for(('battle_setup'), campaign_id=unit.campaign_id))

