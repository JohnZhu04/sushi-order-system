# from typing import List, Any

from fastapi import FastAPI
from app.db import session
from app.model import Sushi, Drink

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/menus/sushi")
def get_sushi_menus(category_id: int = None):
    if category_id:
        sushis = session.query(Sushi).filter(Sushi.category_id == category_id).all()
    else:
        sushis = session.query(Sushi).all()
    return sushis

@app.get("/menus/drink")
def get_drink_menus():
    drinks = session.query(Drink).all()
    return drinks

@app.get("/menus")
def get_menus():
    sushis = session.query(Sushi).all()
    drinks = session.query(Drink).all()
    return {'sushis': sushis, 'drinks': drinks}