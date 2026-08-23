from sqlalchemy import String,Float,Text
from sqlalchemy.orm import Mapped,mapped_column

from app.db.base import Base

class Product(Base):
    __tablename__="products"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    name:Mapped[str]=mapped_column(String(100),nullable=False,index=True)
    description:Mapped[str|None]=mapped_column(Text,nullable=True)
    price:Mapped[float]=mapped_column(Float,nullable=False)
    category:Mapped[str]=mapped_column(String(100),nullable=False,index=True)
    stock:Mapped[int]=mapped_column(default=0,nullable=False)