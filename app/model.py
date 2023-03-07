from datetime import datetime

from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(String(50), primary_key=True)
    seat_id = Column(Integer, ForeignKey('seats.seat_id'))
    seat = relationship('Seat', backref='customers')

class Seat(Base):
    __tablename__ = 'seats'
    seat_id = Column(Integer, primary_key=True)
    is_available = Column(Boolean)

class Sushi(Base):
    __tablename__ = 'sushis'
    sushi_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    has_wasabi = Column(Boolean)
    price = Column(Numeric(10, 2))
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    category = relationship('Category', backref='sushis')

class Drink(Base):
    __tablename__ = 'drinks'
    drink_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Numeric(10, 2))

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), ForeignKey('customers.customer_id'))
    total_price = Column(Numeric(10, 2))
    status = Column(Integer)
    order_details = relationship('OrderDetail', backref='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'
    order_detail_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    item_type = Column(Integer)
    item_id = Column(Integer)
    topping = Column(Integer)
    size = Column(Integer)
    quantity = Column(Integer)
    has_wasabi = Column(Boolean)
    price = Column(Numeric(10, 2))
    status = Column(Integer)
    ordered_at = Column(DateTime)

class Stock(Base):
    __tablename__ = 'stocks'
    stock_id = Column(Integer, primary_key=True)
    item_type = Column(Integer)
    item_id = Column(Integer, nullable=True)
    quantity = Column(Integer)
    sushi_id = Column(Integer, ForeignKey('sushis.sushi_id'), nullable=True)
    sushi = relationship('Sushi', backref='stocks', foreign_keys=[sushi_id])
    drink_id = Column(Integer, ForeignKey('drinks.drink_id'), nullable=True)
    drink = relationship('Drink', backref='stocks', foreign_keys=[drink_id])

    __mapper_args__ = {
        'polymorphic_on': item_type,
        'polymorphic_identity': 0,
    }
