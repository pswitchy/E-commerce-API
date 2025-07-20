from fastapi import APIRouter, Body, status, Query
from typing import Optional
import re
from ..database import product_collection
from ..models import Product

router = APIRouter()

@router.post("/products", response_description="Add new product", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product = Body(...)):
    """
    Creates a new product in the database.
    """
    product_dict = product.model_dump(by_alias=True, exclude=["id"])
    new_product = await product_collection.insert_one(product_dict)
    return {"id": str(new_product.inserted_id)}

@router.get("/products", response_description="List all products")
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name (case-insensitive, partial match)"),
    size: Optional[str] = Query(None, description="Filter by available size"),
    limit: int = Query(10, ge=1, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip")
):
    query = {}
    if name:
        query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
    if size:
        query["sizes.size"] = size

    products_cursor = product_collection.find(query, {"sizes": 0}).skip(offset).limit(limit)
    products = await products_cursor.to_list(length=limit)

    for prod in products:
        prod["id"] = str(prod["_id"])
        del prod["_id"]

    next_page_url = None
    if len(products) == limit:
      next_offset = offset + limit
      next_page_url = f"/products?limit={limit}&offset={next_offset}"

    previous_page_url = None
    if offset > 0:
      previous_offset = offset - limit
      if previous_offset < 0:
          previous_offset = 0
      previous_page_url = f"/products?limit={limit}&offset={previous_offset}"


    return {
        "data": products,
        "page": {
            "next": next_page_url,
            "limit": limit,
            "previous": previous_page_url
        }
    }