from typing import Annotated

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter,Depends,HTTPException,status

from app.models.user import User
from app.schemas.user import UserResponse
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.auth import RegisterRequest, TokenResponse
from app.services.auth_service import authenticate_user,register_user

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(data:RegisterRequest,db:Annotated[Session,Depends(get_db)]):
    try:
        return register_user(db,data)
    except ValueError as exc:
        raise HTTPException(status_code=400,detail=str(exc))

@router.post("/login",response_model=TokenResponse)
def login(form_data:Annotated[OAuth2PasswordBearer,Depends()],db:Annotated[Session,Depends(get_db)]):
    token=authenticate_user(db,form_data.username,form_data.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid email or password",headers={"WWW-Authenticate":"Bearer"})

    return TokenResponse(access_token=token)

@router.get("/me",response_model=UserResponse)
def me(current_user:Annotated[User,Depends(get_current_user)]):
    return current_user