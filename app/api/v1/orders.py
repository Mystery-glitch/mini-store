from typing import Annotated

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter,HTTPException

from app.models.user import User
from app.models.order import Order
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.schemas.order import OrderCreate,OrderResponse
from app.services.order_service import create_order,get_order

router=APIRouter(prefix="/orders",tags=["Orders"])

@router.post("/",response_model=OrderResponse,status_code=201)
def create(data:OrderCreate,current_user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]):
    try:
        return create_order(db,current_user,data)
    except ValueError as exc:
        raise HTTPException(status_code=404,detail=str(exc))

@router.get("/",response_model=list[OrderResponse])
def list_orders(current_user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]):
    query=select(Order).where(Order.user_id==current_user.id)
    return list(db.scalars(query).all())

@router.get("/{order_id}",response_model=OrderResponse)
def retrieve_order(order_id:int,current_user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]):
    try:
        return get_order(db,order_id,current_user.id)
    except PermissionError as exc:
        raise HTTPException(status_code=404,detail=str(exc))
        