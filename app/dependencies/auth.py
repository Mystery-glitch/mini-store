from typing import Annotated

import jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.dependencies.database import get_db
from app.models.user import User

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token:Annotated[str,Depends(oauth2_scheme)],db:Annotated[Session,Depends(get_db)])->User:
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=decode_access_token(token)
        user_id=payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user=db.get(User,int(user_id))
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Inactive User")

    return user

def require_admin(current_user:Annotated[User,Depends(get_current_user)])->User:
    if current_user.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin access required")

    return current_user