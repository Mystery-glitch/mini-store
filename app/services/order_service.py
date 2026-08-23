from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.order import OrderCreate
from app.models.order import Order,OrderItem
from app.core.exceptions import ProductNotFoundException,InsufficientStockException,OrderNotFoundException

def create_order(db:Session,user_id:int,data:OrderCreate)->Order:
    order=Order(user_id="user_id",total_amount=0,status="pending")
    db.add(order)
    total=0.0
    for item in data.items:
        product=db.get(Product,item.product_id)

        if product is None:
            raise InsufficientStockException(product.id)
        
        product.stock-=item.quantity

        order_item=OrderItem(product_id=product.id,quantity=item.quantity,unit_price=product.price)
        order.items.append(order_item)
        total+=product.price*item.quantity

    order.total_amount=total
    db.commit()
    db.refresh(order)

    return order

def get_order(db:Session,order_id:int,user_id:int)->Order:
    order=db.get(Order,order_id)
    if order is None:
        raise OrderNotFoundException(order_id)
    if order.user_id!=user_id:
        raise PermissionError("You cannot access this order")

    return order