from publications.models.publication import Publication as PublicationModel
from publications.schemas.publication import Publication

class PublicationService():
    def __init__(self, db) -> None:
        self.db = db


    def get_publications(self):
        result = self.db.query(PublicationModel).all()
        return result


    def get_publication_by_id(self, id: int):
        result = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        return result


    def create_publication(self, publication: Publication):
        new_publication = PublicationModel(**publication.model_dump())
        self.db.add(new_publication)
        self.db.commit()
        return


    def update_publication(self, id: int, data: Publication):
        publication = self.db.query(PublicationModel).filter(PublicationModel.id == id).first()
        publication.title = data.title
        publication.content = data.content

        self.db.commit()
        return


    def delete_publication(self):
        pass
