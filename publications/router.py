from typing import List
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from publications.schemas.publication import Publication
from publications.models.publication import Publication as PublicationModel


publication_router = APIRouter()



@publication_router.get('/', tags=["publications"], status_code=200, response_model=List[Publication])
def get_publications():
    db = Session()
    result = db.query(PublicationModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@publication_router.post('/', tags=["publications"], status_code=201, response_model=dict)
def create_publication(publication: Publication):
    db = Session()
    new_publication = PublicationModel(**publication.model_dump())
    db.add(new_publication)
    db.commit()

    return JSONResponse(
        status_code=201,
        content="Publication created successfully"
    )
