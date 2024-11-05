
from fastapi.encoders import jsonable_encoder
from publications.models.publication import Publication
from publications.schemas.publication import PublicationResponse
from users.models.user import User as UserModel
from users.schemas.user import User, UserRegister
from core.security import get_password_hash


class UserService:
    def __init__(self, db):
        self.db = db


    def register(self, user: UserRegister):
        hashed_password = get_password_hash(user.password)
        
        new_user = UserModel(
            name=user.name,
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return


    def get_user_by_id(self, id: int):
        result = self.db.query(UserModel).filter(UserModel.id == id).first()
        return result


    def get_user_by_email(self, email: str):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        return result


    def get_user_by_username(self, username: str):
        result = self.db.query(UserModel).filter(UserModel.username == username).first()
        return result


    def update_user(self, id: int, data: User):
        user = self.db.query(UserModel).filter(UserModel.id == id).first()
        user.name = data.name
        user.username = data.username
        user.email = data.email

        self.db.commit()
        return

    def get_publication_by_username(self, username: str):
        results = self.db.query(Publication).join(UserModel).filter(UserModel.username == username).all()
        publications = []
        for publication in results:
            p = PublicationResponse(
                **jsonable_encoder(publication),
                author=publication.user.name
            )
            publications.append(p)
        return publications