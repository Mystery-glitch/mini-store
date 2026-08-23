from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.db.base import Base

class User(Base):
    __tablename__="users"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True,nullable=False)
    hashed_password:Mapped[str]=mapped_column(String(255),nullable=False)
    role:Mapped[str]=mapped_column(String(50),default="customer",nullable=False)
    is_active:Mapped[bool]=mapped_column(default=True,nullable=False)

    orders=relationship("Order",back_populates="user",cascade="all, delete-orphan")