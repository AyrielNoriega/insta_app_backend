from publications.models.publication import Publication as PublicationModel
from publications.schemas.publication import Publication

class PublicationService():
    def __init__(self, db) -> None:
        self.db = db


    def get_publications(self):
        result = self.db.query(PublicationModel).all()
        return result


    def create_publication(self, publication: Publication):
        new_publication = PublicationModel(**publication.model_dump())
        self.db.add(new_publication)
        self.db.commit()
        return


    def update_publication(self):
        pass


    def delete_publication(self):
        pass
