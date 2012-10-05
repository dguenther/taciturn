import taciturn
from webapp import db

unit_battles = db.Table('unit_battles',
    db.Column('unit_id', db.Integer, db.ForeignKey('unit.id')),
    db.Column('battle_id', db.Integer, db.ForeignKey('battle.id'))
)

class Unit(taciturn.Unit, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    speed = db.Column(db.Integer)
    ct = db.Column(db.Integer)
    order_num = db.Column(db.Integer)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    
    #statuses = []
    #slow_action = None

    def __init__(self, campaign_id, battles=[]):
        self.campaign_id = campaign_id
        self.battles = battles
        
    def __repr__(self):
        return '<Unit %s>' % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    campaigns = db.relationship('Campaign', backref='owner')
    def __init__(self, email):
        self.email = email
    def __repr__(self):
        return '<User %s>' % self.id

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    battles = db.relationship('Battle', backref='campaign')
    units = db.relationship('Unit', backref='campaign')
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<Campaign %s>' % self.id

class Battle(taciturn.Battle, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    units = db.relationship('Unit', secondary=unit_battles, backref=db.backref('battles'))
    def __init__(self, campaign_id):
        self.campaign_id = campaign_id

    def __repr__(self):
        return '<Battle %s>' % self.id
