from typing import List
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.database import Session
from publications.schemas.publication import Publication
from publications.service import PublicationService


publication_router = APIRouter()
publication_router.prefix = "/publications"



@publication_router.get('/', tags=["publications"], status_code=200, response_model=List[Publication])
def get_publications():
    db = Session()
    result = PublicationService(db).get_publications()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@publication_router.get('/{id}', tags=["publications"], status_code=200, response_model=Publication)
def get_publications(id: int):
    db = Session()
    result = PublicationService(db).get_publication_by_id(id)
    if not result:
        content = {"message": "Publication not found"}
        status = 404
    else:
        content = result
        status = 200
    return JSONResponse(status_code=status, content=jsonable_encoder(content))


@publication_router.post('/', tags=["publications"], status_code=201, response_model=dict)
def create_publication(publication: Publication):
    db = Session()
    PublicationService(db).create_publication(publication)


    return JSONResponse(
        status_code=201,
        content="Publication created successfully"
    )


@publication_router.put('/{id}', tags=["publications"], status_code=200, response_model=dict)
def update_publication(id: int, publication: Publication):
    db = Session()
    result = PublicationService(db).get_publication_by_id(id)
    if not result:
        content = {"message": "Publication not found"}
        status = 404
    else:
        PublicationService(db).update_publication(id, publication)
        content = "Publication updated successfully"
        status = 200

    return JSONResponse(
        status_code=status,
        content=content
    )


@publication_router.delete('/{id}', tags=["publications"], status_code=204)
def delete_publication(id: int) -> JSONResponse:
    db = Session()
    result = PublicationService(db).get_publication_by_id(id)
    if not result:
        content = {"message": "Publication not found"}
        status = 404
    else:
        PublicationService(db).delete_publication(id)
        content = None
        status = 204

    return JSONResponse(
        status_code=status,
        content=content
    )
