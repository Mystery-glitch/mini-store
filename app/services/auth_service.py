from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.core.security import create_access_token,hash_password,verify_password

def register_user(db:Session,data:RegisterRequest)->User:
    existing=db.scalar(select(User).where(User.email==data.email))
    if existing:
        raise ValueError("Email already existing")

    user=User(email=data.email,hashed_password=hash_password(data.password),role="customer")
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db:Session,email:str,password:str)->str|None:
    user=db.scalar(select(User).where(User.email==email))

    if user is None:
        return None

    if not verify_password(password,user.hashed_password):
        return None

    return create_access_token(subject=str(user.id),role=user.role)