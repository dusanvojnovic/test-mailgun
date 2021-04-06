from ma import ma
from models.album import AlbumModel
from models.artist import ArtistModel

class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AlbumModel
        load_only = ("artist","artist_id")
        dump_only = ("id",)
        include_fk = True
        load_instance = True
