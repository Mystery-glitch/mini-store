from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.product import Product
from app.schemas.product import ProductCreate,ProductUpdate
from app.core.exceptions import ProductNotFoundException

def create_product(db:Session,data:ProductCreate)->Product:
    product=Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_product(db:Session,product_id:int)->Product:
    product=db.get(Product,product_id)
    if product is None:
        raise ProductNotFoundException

    return product

def get_products(db:Session,skip:int,limit:int,category:str|None=None,search:str|None=None,sort:str="id")->list[Product]:
    query=select(Product)
    if category:
        query=query.where(Product.category==category)
    if search:
        query=query.where(Product.name.ilike(f"%{search}%"))

    sort_columns={
        "id":Product.id,
        "name":Product.name,
        "price":Product.price
    }
    column=sort_columns.get(sort,Product.id)
    query=query.order_by(column)

    query=query.offset(skip).limit(limit)

    return list(db.scalars(query).all())

def update_product(db:Session,product_id:int,data:ProductUpdate)->Product:
    product=get_product(db,product_id=product_id)
    update_data=data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product,field,value)

    db.commit()
    db.refresh(product)

def delete_product(db:Session,product_id:int)->None:
    product=get_product(db,product_id=product_id)
    db.delete(product)
    db.commit()