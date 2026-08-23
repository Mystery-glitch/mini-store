from sqlalchemy import ForeignKey,Float,Integer
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.db.base import Base

class Order(Base):
    __tablename__="orders"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False)
    total_amount:Mapped[float]=mapped_column(Float,nullable=False)
    status:Mapped[str]=mapped_column(default="pending",nullable=False)

    user=relationship("User",back_populates="orders")
    items=relationship("OrderItem",back_populates="order",cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__="order_items"

    id:Mapped[int]=mapped_column(primary_key=True)
    order_id:Mapped[int]=mapped_column(ForeignKey("orders.id"),nullable=False)
    product_id:Mapped[int]=mapped_column(ForeignKey("products.id"),nullable=False)
    quantity:Mapped[int]=mapped_column(Integer,nullable=False)
    unit_price:Mapped[float]=mapped_column(Float,nullable=False)

    order=relationship("Order",back_populates="items")