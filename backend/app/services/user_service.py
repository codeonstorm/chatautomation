from typing import List, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate) -> User:
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=user.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_user(self, db: Session, user_id: int, user: UserUpdate) -> User:
        db_user = self.get_user(db, user_id)
        update_data = user.dict(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int) -> None:
        db_user = self.get_user(db, user_id)
        db.delete(db_user)
        db.commit()

