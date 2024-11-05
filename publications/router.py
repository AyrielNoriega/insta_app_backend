from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.database import Session
from publications.schemas.publication import Publication, PublicationInDb, PublicationResponse
from publications.service import PublicationService
from users.schemas.user import User
from users.service import auth


publication_router = APIRouter()
publication_router.prefix = "/publications"
publication_router.tags = ["publications"]



@publication_router.get('/', status_code=200, response_model=List[PublicationResponse])
def get_publications():
    db = Session()
    result = PublicationService(db).get_publications()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@publication_router.get('/{id}', status_code=200, response_model=Publication)
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


@publication_router.post('/', status_code=201, response_model=dict)
def create_publication(
    publication: Publication,
    current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    db = Session()
    PublicationService(db).create_publication(publication, current_user)

    return JSONResponse(
        status_code=201,
        content="Publication created successfully"
    )


@publication_router.put('/{id}', status_code=200, response_model=dict)
def update_publication(
    id: int,
    current_publication: Publication,
    current_user: Annotated[User, Depends(auth.get_current_active_user)]
):
    db = Session()
    publication = PublicationService(db).get_publication_by_id(id)
    if not publication:
        content = {"message": "Publication not found"}
        status_code = 404
    else:
        get_publication = PublicationInDb(**jsonable_encoder(publication))

        if current_user.id != get_publication.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this publication"
            )
        PublicationService(db).update_publication(id, current_publication)
        content = "Publication updated successfully"
        status_code = 200

    return JSONResponse(
        status_code=status_code,
        content=content
    )


@publication_router.delete('/{id}', status_code=204)
def delete_publication(
    id: int,
    current_user: Annotated[User, Depends(auth.get_current_active_user)]
) -> JSONResponse:
    db = Session()
    publication = PublicationService(db).get_publication_by_id(id)

    if not publication:
        content = {"message": "Publication not found"}
        status_code = 404
    else:
        get_publication = PublicationInDb(**jsonable_encoder(publication))

        if current_user.id != get_publication.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this publication"
            )
        PublicationService(db).delete_publication(id)
        content = None
        status_code = 204

    return JSONResponse(
        status_code=status_code,
        content=content
    )
