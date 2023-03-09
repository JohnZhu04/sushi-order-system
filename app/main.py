<<<<<<< HEAD
from typing import List

=======
>>>>>>> 578de4c (Add API: menu CRUD)
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.db import session, Base
from app.model import Sushi, Drink, Customer, Seat, Category, Order, OrderDetail, Stock
import uuid

from pydantic import BaseModel

app = FastAPI()


class SushiModel(BaseModel):
    sushi_id: int
    category_id: int
    name: str
    price: float
    has_wasabi: bool


class DrinkModel(BaseModel):
    drink_id: int
    name: str
    price: float


<<<<<<< HEAD
class OrderItemModel(BaseModel):
    item_type: int
    item_id: int
    topping: int = None
    size: int = None
    quantity: int
    has_wasabi: bool = None


class OrderModel(BaseModel):
    order_items: List[OrderItemModel]


=======
>>>>>>> 578de4c (Add API: menu CRUD)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/menus/sushi")
def get_sushi_menus(category_id: int = None):
    try:
        if category_id:
            sushis = session.query(Sushi).filter(
                Sushi.category_id == category_id).all()
        else:
            sushis = session.query(Sushi).all()
        sushi_menus = []

        for sushi in sushis:
            sushi_menu = {
                'sushi_id': sushi.sushi_id,
                'category_id': sushi.category_id,
                'name': sushi.name,
                'price': str(sushi.price),
                'has_wasabi': sushi.has_wasabi,
            }
            sushi_menus.append(sushi_menu)

        response = {
            'result': {
                'sushi_menus': sushi_menus,
            },
            'errors': [],
        }
        return JSONResponse(content=response)

    except Exception as e:
        response = {
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        }
        return JSONResponse(content=response)


@app.get("/menus/drink")
def get_drink_menus():
    try:
        drinks = session.query(Drink).all()
        drink_menus = []
        for drink in drinks:
            drink_menu = {
                'drink_id': drink.drink_id,
                'name': drink.name,
                'price': str(drink.price),
            }
            drink_menus.append(drink_menu)
        response = {
            'result': {
                'drink_menus': drink_menus,
            },
            'errors': [],
        }
        return JSONResponse(content=response)
    except Exception as e:
        response = {
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        }
        return JSONResponse(content=response)


@app.get("/menus")
def get_menus():
    sushis = session.query(Sushi).all()
    drinks = session.query(Drink).all()
    sushi_menus = []
    drink_menus = []
    for sushi in sushis:
        sushi_menu = {
            'sushi_id': sushi.sushi_id,
            'category_id': sushi.category_id,
            'name': sushi.name,
            'price': str(sushi.price),
            'has_wasabi': sushi.has_wasabi,
        }
        sushi_menus.append(sushi_menu)
    for drink in drinks:
        drink_menu = {
            'drink_id': drink.drink_id,
            'name': drink.name,
            'price': str(drink.price),
        }
        drink_menus.append(drink_menu)
    response = {
        'result': {
            'sushi_menus': sushi_menus,
            'drink_menus': drink_menus,
        },
        'errors': [],
    }
    return JSONResponse(content=response)


@app.post("/customers")
def create_customer(seat_id: int):
    try:
        seat = session.query(Seat).filter(Seat.seat_id == seat_id).first()
        if not seat.is_available:
            return JSONResponse(content={
                'result': {},
                'errors': [
                    {
                        'error_code': 400,
                        'error_message': 'This seat is already taken.',
                    }
                ]
            })

        # generate customer_id by UUID
        customer_id = uuid.uuid4()

        # insert customer_id and seat_id into customers table
        new_customer = Customer(customer_id=customer_id, seat_id=seat_id)
        session.add(new_customer)
        session.commit()

        # update seat_id to unavailable
        seat = session.query(Seat).filter(Seat.seat_id == seat_id).first()
        seat.is_available = False
        session.commit()

        response = {
            'result': {
                'customer_id': str(customer_id),
            },
            'errors': [],
        }
        return JSONResponse(content=response)

    except Exception as e:
        response = {
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        }
        return JSONResponse(content=response)


@app.get("/customers/{customer_id}/orders")
def get_customer_orders(customer_id: str):
    pass


@app.post("/customers/{customer_id}/orders")
def create_customer_order(customer_id: str, order: dict):
    pass


@app.get("/admin/orders/new")
def get_new_orders():
    pass


@app.get("/admin/orders")
def get_orders_by_customer_id(customer_id: str):
    pass


@app.put("/admin/order_details/{order_detail_id}")
def update_order_detail(order_detail_id: int, status: int):
    pass


@app.post("/admin/menus/sushi")
def create_sushi_menu(sushi: SushiModel):
    try:
        _sushi = Sushi(sushi_id=sushi.sushi_id, category_id=sushi.category_id,
                       name=sushi.name, price=sushi.price, has_wasabi=sushi.has_wasabi)
        session.add(_sushi)
        _stock = Stock(item_type=0, item_id=sushi.sushi_id, quantity=0)
        session.add(_stock)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return JSONResponse(content={
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        })


@app.put("/admin/menus/sushi/{sushi_id}")
def update_sushi_menu(sushi_id: int, sushi: SushiModel):
    try:
        _sushi = session.query(Sushi).filter(
            Sushi.sushi_id == sushi_id).first()
        _sushi.name = sushi.name
        _sushi.price = sushi.price
        _sushi.has_wasabi = sushi.has_wasabi
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return JSONResponse(content={
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        })


@app.delete("/admin/menus/sushi/{sushi_id}")
def delete_sushi_menu(sushi_id: int):
    try:
        _sushi = session.query(Sushi).filter(
            Sushi.sushi_id == sushi_id).first()
        session.delete(_sushi)
        _stock = session.query(Stock).filter(Stock.item_type == 0).filter(
            Stock.item_id == sushi_id).first()
        session.delete(_stock)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return JSONResponse(content={
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        })


@app.post("/admin/menus/drink")
def create_drink_menu(drink: DrinkModel):
    try:
        _drink = Drink(drink_id=drink.drink_id,
                       name=drink.name, price=drink.price)
        session.add(_drink)
        _stock = Stock(item_type=1, item_id=drink.drink_id, quantity=0)
        session.add(_stock)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return JSONResponse(content={
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        })


@app.put("/admin/menus/drink/{drink_id}")
def update_drink_menu(drink_id: int, drink: DrinkModel):
    try:
        _drink = session.query(Drink).filter(
            Drink.drink_id == drink_id).first()
        _drink.name = drink.name
        _drink.price = drink.price
        session.commit()
        return None
    except Exception as e:
        return JSONResponse(content={
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        })


@app.delete("/admin/menus/drink/{drink_id}")
def delete_drink_menu(drink_id: int):
    try:
        _drink = session.query(Drink).filter(
            Drink.drink_id == drink_id).first()
        session.delete(_drink)
        _stock = session.query(Stock).filter(Stock.item_type == 1).filter(
            Stock.item_id == drink_id).first()
        session.delete(_stock)
        session.commit()
        return None
    except Exception as e:
        session.rollback()
        return JSONResponse(content={
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        })
