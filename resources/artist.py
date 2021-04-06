from flask_restful import Resource
from flask import request

from models.artist import ArtistModel
from schemas.artist import ArtistSchema

artist_schema = ArtistSchema()
artist_list_schema = ArtistSchema(many = True)

class Artist(Resource):
    @classmethod
    def get(cls, name):
        artist = ArtistModel.find_by_name(name)
        if artist:
            return artist_schema.dump(artist), 200
        return {'message': 'There is no artist with that name'}, 404

    @classmethod
    def post(cls, name):
        if ArtistModel.find_by_name(name):
            return {'message': "Artist already exists"}

        artist = ArtistModel(name = name)
        try:
            artist.save_to_db()
        except:
            return {'message': 'An error occurred while adding the artist'}, 500

        return artist_schema.dump(artist)

    @classmethod
    def put(cls, name):
        artist_json = request.get_json()
        artist = ArtistModel.find_by_name(name)

        if artist:
            artist.genre = artist_json['genre']
        else:
            artist_json['name'] = name
            artist = artist_schema.load(artist_json)

        artist.save_to_db()

        return artist_schema.dump(artist), 200

    @classmethod
    def delete(cls, name):
        artist = ArtistModel.find_by_name(name)
        if artist:
            artist.delete_from_db()
            return {'message': 'Artist successfully removed'}, 200
        return {'message': 'There is no artist with that name'}, 404



class AllArtists(Resource):
    @classmethod
    def get(cls):
        return {'artists': artist_list_schema.dump(ArtistModel.find_all())}, 200
