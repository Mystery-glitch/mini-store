from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter,Query,status

from app.models.user import User
from app.dependencies.database import get_db
from app.dependencies.common import pagination
from app.dependencies.auth import require_admin
from app.schemas.product import ProductCreate,ProductUpdate,ProductResponse
from app.services.product_service import create_product,delete_product,get_product,get_products,update_product

router=APIRouter(prefix="/products",tags=["Products"])

@router.get("/",response_model=list[ProductResponse])
def list_products(db:Annotated[Session,Depends(get_db)],page:Annotated[dict,Depends(pagination)],category:str|None=None,search:str|None=None,sort:str=Query(default="id",pattern="^(id|name|price)$")):
    return get_products(db=db,skip=page["skip"],limit=page["limit"],category=category,search=search,sort=sort)

@router.get("/product_id",response_model=ProductResponse)
def retrieve_product(product_id:int,db:Annotated[Session,Depends(get_db)]):
    return get_product(db=db,product_id=product_id)

@router.post("/",response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
def create(data:ProductCreate,db:Annotated[Session,Depends(get_db)],_:Annotated[User,Depends(require_admin)]):
    return create_product(db,data)

@router.patch("/{product_id}",response_model=ProductResponse,)
def update(product_id: int,data: ProductUpdate,db: Annotated[Session, Depends(get_db)],_: Annotated[User,Depends(require_admin)]):
    return update_product(db,product_id,data)

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: int,db: Annotated[Session, Depends(get_db)],_: Annotated[User,Depends(require_admin)]):
    delete_product(db,product_id)