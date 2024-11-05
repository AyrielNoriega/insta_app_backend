from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload

from publications.models.publication import Publication as PublicationModel
from publications.schemas.publication import Publication, PublicationResponse
from users.schemas.user import User
from users.models.user import User as UserModel

class PublicationService():
    def __init__(self, db) -> None:
        self.db = db


    def get_publications(self):
        # result = self.db.query(PublicationModel).all()
        #realizar una consulta a relacion de usuario
        result = (
            self.db.query(PublicationModel)
            .options(joinedload(PublicationModel.user))
            .all()
        )
        publications = []
        for publication in result:
            p = PublicationResponse(
                **jsonable_encoder(publication),
                author=publication.user.name
            )
            publications.append(p)

        return publications


    def get_publication_by_id(self, id: int):
        result = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        return result


    def create_publication(self, publication: Publication, current_user: User):
        new_publication = PublicationModel(**publication.model_dump(), user_id=current_user.id)
        self.db.add(new_publication)
        self.db.commit()
        return


    def update_publication(self, id: int, data: Publication):
        publication = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        publication.title = data.title
        publication.content = data.content

        self.db.commit()
        return


    def delete_publication(self, id: int):
        publication = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        self.db.delete(publication)
        self.db.commit()
        return
