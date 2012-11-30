import taciturn
from webapp import db

from sqlalchemy.orm import validates

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
    statuses = db.relationship('Status', backref=db.backref('unit'))
    slow_action = db.relationship('SlowAction', uselist=False, backref=db.backref('unit'))

    def __init__(self, campaign_id, battles=[]):
        self.campaign_id = campaign_id
        self.battles = battles

    def __repr__(self):
        return '<Unit %s: %s>' % (self.id, self.name)

    @validates('speed')
    def validate_speed(self, key, speed):
        return int(speed)

    @validates('ct')
    def validate_ct(self, key, ct):
        return int(ct)

    @validates('order_num')
    def validate_order_num(self, key, order_num):
        return int(order_num)


class Status(taciturn.Status, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    duration = db.Column(db.Integer)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))


class SlowAction(taciturn.SlowAction, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    charge_ticks = db.Column(db.Integer)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))


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
    name = db.Column(db.String(40), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    battles = db.relationship('Battle', backref='campaign')
    units = db.relationship('Unit', backref='campaign')

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<Campaign %s: %s>' % (self.id, self.name)


class Battle(taciturn.Battle, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    units = db.relationship('Unit', secondary=unit_battles, backref=db.backref('battles'))

    def __init__(self, campaign_id):
        self.campaign_id = campaign_id

    def __repr__(self):
        return '<Battle %s: %s>' % (self.id, self.name)
