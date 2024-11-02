
from users.models.user import User as UserModel
from users.schemas.user import User, UserRegister


class UserService:
    def __init__(self, db):
        self.db = db


    def register(self, user: UserRegister):
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        return


    def get_user_by_id(self, id: int):
        result = self.db.query(UserModel).filter(UserModel.id == id).first()
        return result


    def get_user_by_email(self, email: str):
        result = self.db.query(UserModel).filter(UserModel.email == email).first()
        return result


    def update_user(self, id: int, data: User):
        user = self.db.query(UserModel).filter(UserModel.id == id).first()
        user.name = data.name
        user.email = data.email

        self.db.commit()
        return
