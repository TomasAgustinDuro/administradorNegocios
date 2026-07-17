from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__="products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

class Inventory(Base):
    __tablename__="inventory"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    reason = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

class Sales(Base):
    __tablename__="sales"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False, default=0)
    date = Column(DateTime, nullable=False)
    status = Column(String, nullable=True)

    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__="sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    sale = relationship("Sales", back_populates="items")