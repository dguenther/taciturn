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

