from db import db

class AlbumModel(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    year = db.Column(db.Integer, nullable = False)

    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable = False)
    artist = db.relationship("ArtistModel")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()

    @classmethod
    def find_by_artist(cls, name):
        return cls.query.filter_by(artist = name).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.comit()