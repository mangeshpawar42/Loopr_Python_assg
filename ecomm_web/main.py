from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.security import HTTPBearer
from authentication import authenticate_user, create_access_token, get_current_user
from cart import create_product, update_product, delete_product, get_cart
from models import Product

app = FastAPI()
security = HTTPBearer()


@app.post("/login")
def login(username: str, password: str):
    if authenticate_user(username, password):
        access_token = create_access_token(username)
        return {"access_token": access_token}
    return {"message": "Invalid username or password"}


@app.post("/cart")
def add_to_cart(product: Product, current_user: str = Depends(get_current_user)):
    create_product(current_user, product)
    return {"message": "Product added to cart"}


@app.put("/cart")
def update_cart(product: Product, current_user: str = Depends(get_current_user)):
    update_product(current_user, product)
    return {"message": "Cart updated"}


@app.delete("/cart/{product_id}")
def remove_from_cart(product_id: str, current_user: str = Depends(get_current_user)):
    delete_product(current_user, product_id)
    return {"message": "Product removed from cart"}


@app.get("/cart")
def view_cart(current_user: str = Depends(get_current_user)):
    cart = get_cart(current_user)
    return {"cart": cart}