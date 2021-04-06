import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from ma import ma
from resources.artist import Artist, AllArtists 
from resources.album import Album, AlbumList
from resources.user import User,UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.confirmation import Confirmation, ConfirmationByUser

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = os.environ.get("APP_SECRET_KEY")

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return (jwt_headers["alg"] in BLACKLIST)

api.add_resource(Artist, '/artists/<string:name>')
api.add_resource(AllArtists, '/artists')
api.add_resource(Album, '/albums/<string:name>')
api.add_resource(AlbumList, '/albums')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout/')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ConfirmationByUser, '/confirmation/user/<int:user_id>')
api.add_resource(Confirmation, '/user_confirmation/string:confirmation_id')


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)