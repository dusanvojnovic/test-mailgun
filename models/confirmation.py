from db import db
from uuid import uuid4
from time import time

CONFIRMATION_EXPIRATION_DELTA = 1800 # 30 min

class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(50), primary_key = True) #string, because its gonna be a token
    expire_at = db.Column(db.Integer, nullable = False)
    confirmed = db.Column(db.Boolean, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('UserModel')

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex  # universaly unique id
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()

    # function isnt modifing things, just calculate value
    @property
    def expired(self):
        return time() > self.expire_at # current time > time when created + confirmation delta

    def force_to_exipre(self):
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.add(self)
        db.session.commit()