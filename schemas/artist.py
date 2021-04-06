from ma import ma
from models.artist import ArtistModel
from models.album import AlbumModel
from schemas.album import AlbumSchema

class ArtistSchema(ma.SQLAlchemyAutoSchema):
    albums = ma.Nested(AlbumSchema, many = True)
    class Meta:
        model = ArtistModel
        load_only = ("id",)
        dump_only = ("albums",)
        include_fk = True
        load_instance = True
