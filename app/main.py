from typing import List

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


class OrderItemModel(BaseModel):
    item_type: int
    item_id: int
    topping: int = None
    size: int = None
    quantity: int
    has_wasabi: bool = None


class OrderModel(BaseModel):
    order_items: List[OrderItemModel]


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
        return JSONResponse(content=response, status_code=500)


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
        return JSONResponse(content=response, status_code=500)


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
        if not seat:
            return JSONResponse(content={
                'result': {},
                'errors': [
                    {
                        'error_code': 400,
                        'error_message': 'This seat does not exist.',
                    }
                ]
            }, status_code=400)
        
        if not seat.is_available:
            return JSONResponse(content={
                'result': {},
                'errors': [
                    {
                        'error_code': 400,
                        'error_message': 'This seat is already taken.',
                    }
                ]
            }, status_code=400)

        # generate customer_id by UUID
        customer_id = uuid.uuid4()

        # insert customer_id and seat_id into customers table
        new_customer = Customer(customer_id=customer_id, seat_id=seat_id)
        session.add(new_customer)

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
        session.rollback()
        response = {
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        }
        return JSONResponse(content=response, status_code=500)


@app.get("/customers/{customer_id}/orders")
def get_customer_orders(customer_id: str):
    try:
        _orders = session.query(Order).filter(
            Order.customer_id == customer_id).all()
        orders = []
        
        for order in _orders:
            _order_detail = session.query(OrderDetail).filter(
                OrderDetail.order_id == order.order_id).all()
            order_details = []

            for order_detail in _order_detail:
                if order_detail.item_type == 0:
                    order_details.append({
                        'order_detail_id': order_detail.order_detail_id,
                        'item_type': order_detail.item_type,
                        'item_id': order_detail.item_id,
                        'topping': order_detail.topping,
                        'size': order_detail.size,
                        'quantity': order_detail.quantity,
                        'has_wasabi': order_detail.has_wasabi,
                        'price': str(order_detail.price),
                        'status': order_detail.status,
                        'ordered_at': str(order_detail.ordered_at),
                    })
                else:
                    order_details.append({
                        'order_detail_id': order_detail.order_detail_id,
                        'item_type': order_detail.item_type,
                        'item_id': order_detail.item_id,
                        'quantity': order_detail.quantity,
                        'price': str(order_detail.price),
                        'status': order_detail.status,
                        'ordered_at': str(order_detail.ordered_at),
                    })
            
            # compute total price
            total_price = 0
            for order_detail in order_details:
                total_price += float(order_detail['price']) * order_detail['quantity']
            

            orders.append({
                'order_id': order.order_id,
                'customer_id': order.customer_id,
                'status': order.status,
                'total_price': total_price,
                'order_items': order_details
            })

        response = {
            'result': {
                'orders': orders,
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
        return JSONResponse(content=response, status_code=500)


@app.post("/customers/{customer_id}/orders")
def create_customer_order(customer_id: str, order: OrderModel):
    try:
        # insert a new order to orders table and get the order_id
        new_order = Order(customer_id=customer_id, status=0, total_price=0)
        session.add(new_order)
        session.flush()
        order_id = new_order.order_id
        # create order_details
        for order_item in order.order_items:
            # only sushi has topping, size and has_wasabi
            if order_item.item_type == 0:
                sushi = session.query(Sushi).filter(
                    Sushi.sushi_id == order_item.item_id).first()
                price = sushi.price * order_item.quantity
                _order_detail = OrderDetail(
                    order_id=order_id,
                    item_type=order_item.item_type,
                    item_id=order_item.item_id,
                    topping=order_item.topping,
                    size=order_item.size,
                    quantity=order_item.quantity,
                    has_wasabi=order_item.has_wasabi,
                    price=price,
                    status=1
                )
            else:
                drink = session.query(Drink).filter(
                    Drink.drink_id == order_item.item_id).first()
                price = drink.price * order_item.quantity
                _order_detail = OrderDetail(
                    order_id=order_id,
                    item_type=order_item.item_type,
                    item_id=order_item.item_id,
                    quantity=order_item.quantity,
                    price=price,
                    status=1
                )
            session.add(_order_detail)
        session.commit()

    except Exception as e:
        session.rollback()
        response = {
            'result': {},
            'errors': [
                {
                    'error_code': 500,
                    'error_message': str(e),
                }
            ]
        }
        return JSONResponse(content=response, status_code=500)


@app.get("/admin/orders/new")
def get_new_orders():
    # new order: order_details.status == 1
    try:
        # get all new orders, order_details.status == 1
        # order_details join orders join customers join seats
        order_details = session.query(OrderDetail).filter(
            OrderDetail.status == 1).all()

        orders = []
        for order_detail in order_details:
            # find which order this order_detail belongs to
            order = session.query(Order).filter(
                Order.order_id == order_detail.order_id).first()
            # find which customer this order belongs to
            customer = session.query(Customer).filter(
                Customer.customer_id == order.customer_id).first()
            # find which seat this order belongs to
            seat = session.query(Seat).filter(
                Seat.seat_id == customer.seat_id).first()

            order = {
                'order_id': order.order_id,
                'seat_id': seat.seat_id,
                'order_detail_id': order_detail.order_detail_id,
                'customer_id': customer.customer_id,
                'item_type': order_detail.item_type,
                'item_id': order_detail.item_id,
                'topping': order_detail.topping,
                'size': order_detail.size,
                'quantity': order_detail.quantity,
                'has_wasabi': order_detail.has_wasabi,
                'price': str(order_detail.price),
                'status': order_detail.status,
                'ordered_at': str(order_detail.ordered_at),
            }
            orders.append(order)
        response = {
            'result': {
                'orders': orders
            },
            'errors': []
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
        return JSONResponse(content=response, status_code=500)



@app.get("/admin/orders")
def get_orders_by_customer_id(customer_id: str):
    try:
        _orders = session.query(Order).filter(
            Order.customer_id == customer_id).all()
        orders = []
        
        for order in _orders:
            _order_detail = session.query(OrderDetail).filter(
                OrderDetail.order_id == order.order_id).all()
            order_details = []

            for order_detail in _order_detail:
                if order_detail.item_type == 0:
                    order_details.append({
                        'order_detail_id': order_detail.order_detail_id,
                        'item_type': order_detail.item_type,
                        'item_id': order_detail.item_id,
                        'topping': order_detail.topping,
                        'size': order_detail.size,
                        'quantity': order_detail.quantity,
                        'has_wasabi': order_detail.has_wasabi,
                        'price': str(order_detail.price),
                        'status': order_detail.status,
                        'ordered_at': str(order_detail.ordered_at),
                    })
                else:
                    order_details.append({
                        'order_detail_id': order_detail.order_detail_id,
                        'item_type': order_detail.item_type,
                        'item_id': order_detail.item_id,
                        'quantity': order_detail.quantity,
                        'price': str(order_detail.price),
                        'status': order_detail.status,
                        'ordered_at': str(order_detail.ordered_at),
                    })
            
            # compute total price
            total_price = 0
            for order_detail in order_details:
                total_price += float(order_detail['price']) * order_detail['quantity']
            

            orders.append({
                'order_id': order.order_id,
                'customer_id': order.customer_id,
                'status': order.status,
                'total_price': total_price,
                'order_items': order_details
            })

        response = {
            'result': {
                'orders': orders,
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
        return JSONResponse(content=response, status_code=500)


@app.put("/admin/order_details/{order_detail_id}")
def update_order_detail(order_detail_id: int, status: int):
    try:
        order_detail = session.query(OrderDetail).filter(
            OrderDetail.order_detail_id == order_detail_id).first()
        order_detail.status = status
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
        }, status_code=500)


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
        }, status_code=500)


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
        }, status_code=500)


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
        }, status_code=500)


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
        }, status_code=500)


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
        }, status_code=500)


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
        }, status_code=500)
