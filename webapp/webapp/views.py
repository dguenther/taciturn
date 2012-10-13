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
    session.pop('user_id', None)
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

@app.route('/campaign/new', methods=['GET'])
def new_campaign():
    return render_template('new_campaign.html')
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
    return render_template('edit_campaign.html', campaign=campaign)
@app.route('/campaign/edit/<int:campaign_id>', methods=['POST'])
def edit_campaign_post(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    campaign.name = request.form['name']
    db.session.commit()
    return redirect(url_for('view_campaign', campaign_id=campaign.id))

@app.route('/campaign/<int:campaign_id>', methods=['GET'])
def view_campaign(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    units = Unit.query.filter_by(campaign_id=campaign.id).all()
    return render_template('view_campaign.html', campaign=campaign, units=units)

@app.route('/campaign/<int:campaign_id>/unit/new', methods=['GET'])
def new_unit(campaign_id):
    return render_template('edit_unit_form.html', unit=None, campaign_id=campaign_id)
@app.route('/campaign/<int:campaign_id>/unit/edit/<int:unit_id>', methods=['GET'])
def edit_unit(campaign_id, unit_id):
    unit = Unit.query.filter_by(id=unit_id).first_or_404()
    return render_template('edit_unit.html', unit=unit, campaign_id=campaign_id)
@app.route('/campaign/<int:campaign_id>/unit/edit', methods=['POST'])
def edit_unit_post(campaign_id):
    unit_id = request.form['unit_id']
    if unit_id is None:
        unit = Unit(campaign_id=campaign_id)
    else:
        unit = Unit.query.filter_by(id=unit_id).first()
    assert unit.campaign_id == campaign_id
    unit.name = request.form['name']
    unit.speed = request.form['speed']
    unit.ct = request.form['ct']
    db.session.commit()
    return redirect(url_for('view_campaign', campaign_id=campaign_id))


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

