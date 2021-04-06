from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from models.album import AlbumModel
from schemas.album import AlbumSchema
from models.artist import ArtistModel

album_schema = AlbumSchema()
album_list_schema = AlbumSchema(many = True)

class Album(Resource):
    @classmethod
    def get(cls, name):
        album = AlbumModel.find_by_name(name)
        if album:
            return album_schema.dump(album), 200
        return {'message': 'There is no album with that name'}, 404

    @classmethod
    def post(cls, name):
        if AlbumModel.find_by_name(name):
            return {'message': 'Album with that name already exists'}

        album_json = request.get_json()
        album_json['name'] = name 

        album = album_schema.load(album_json)
        try:
            album.save_to_db()
        except:
            return {'message': 'An error occurred while adding the album'}, 500

        return album_schema.dump(album)

    @classmethod
    def put(cls, name):
        album_json = request.get_json()
        album = AlbumModel.find_by_name(name)

        if album:
            album.year = album_json['year']
        else:
            album_json['name'] = name
            album = album_schema.load(album_json)
        
        album.save_to_db()

        return album_schema.dump(album), 200
    
    @jwt_required(fresh=True)
    @classmethod
    def delete(cls, name):
        album = AlbumModel.find_by_name(name)
        if album:
            album.delete_from_db()
            return {'message': 'Album removed'}
        return {'message': 'There is no album with that name'}

class AlbumList(Resource):
    @classmethod
    def get(cls):
        return {"albums": album_list_schema.dump(AlbumModel.find_all())}
        
        