from typing import Dict
from models import Product

# Replace with your logic to fetch cart data from the database
carts = {}


def create_product(user_id: str, product: Product):
    if user_id in carts:
        cart = carts[user_id]
    else:
        cart = []
    cart.append(product.dict())
    carts[user_id] = cart


def update_product(user_id: str, updated_product: Product):
    if user_id in carts:
        cart = carts[user_id]
        for product in cart:
            if product["product_id"] == updated_product.product_id:
                product.update(updated_product.dict())
                break


def delete_product(user_id: str, product_id: str):
    if user_id in carts:
        cart = carts[user_id]
        for product in cart:
            if product["product_id"] == product_id:
                cart.remove(product)
                break


def get_cart(user_id: str) -> Dict[str, any]:
    return {"products": carts.get(user_id, [])}