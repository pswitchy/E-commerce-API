from pydantic import BaseModel, Field
from typing import List, Optional

class Size(BaseModel):
    size: str
    quantity: int

class Product(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    price: float
    sizes: List[Size]

class OrderItem(BaseModel):
    productId: str
    qty: int

class Order(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    userId: str
    items: List[OrderItem]
    total: Optional[float] = None