from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    image: str
    name: str
    price: float
    quantity: int