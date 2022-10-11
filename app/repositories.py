from sqlalchemy.orm import Session
from .models import User


class UserRepository:

    @staticmethod
    def get_users(db: Session) -> list[User]:
        return db.query(User).all()

    @staticmethod
    def get_user_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def user_save(db: Session, user: User) -> User:
        if user.id:
            db.merge(user)
        else:
            db.add(user)
        db.commit()
        return user

    @staticmethod
    def delete_user(db: Session, id: int) -> None:
        user = db.query(User).filter(User.id == id).first()
        if user is not None:
            db.delete(user)
            db.commit()