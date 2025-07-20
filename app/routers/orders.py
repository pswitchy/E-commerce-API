from fastapi import APIRouter, Body, HTTPException, status, Query
from bson import ObjectId

from ..database import order_collection, product_collection
from ..models import Order

router = APIRouter()

@router.post("/orders", response_description="Create a new order", status_code=status.HTTP_201_CREATED)
async def create_order(order: Order = Body(...)):
    total = 0
    for item in order.items:
        try:
            product_id = ObjectId(item.productId)
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid productId format: {item.productId}")

        product = await product_collection.find_one({"_id": product_id})
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {item.productId} not found")
        
        total += product["price"] * item.qty
    
    order.total = total
    order_dict = order.model_dump(by_alias=True, exclude=["id"])
    for item in order_dict["items"]:
        item["productId"] = ObjectId(item["productId"])

    new_order = await order_collection.insert_one(order_dict)
    return {"id": str(new_order.inserted_id)}


@router.get("/orders/{user_id}", response_description="List orders for a user")
async def list_user_orders(user_id: str, limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    """
    Lists all orders for a given user. This pipeline assumes the productId in
    the 'orders' collection is stored correctly as an ObjectId.
    """
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": -1}},
        {"$skip": offset},
        {"$limit": limit},
        
        {"$unwind": "$items"},
        
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",  
                "foreignField": "_id",            
                "as": "productDetails"
            }
        },
        
        {"$unwind": "$productDetails"},
        
        {
            "$group": {
                "_id": "$_id",
                "total": {"$first": "$total"},
                "items": {"$push": {"qty": "$items.qty", "productDetails": "$productDetails"}}
            }
        },
        
        {
            "$project": {
                "_id": 0,
                "id": {"$toString": "$_id"},
                "total": "$total",
                "items": {
                    "$map": {
                        "input": "$items",
                        "as": "item",
                        "in": {
                            "qty": "$$item.qty",
                            "productDetails": {
                                "name": "$$item.productDetails.name",
                                "id": {"$toString": "$$item.productDetails._id"}
                            }
                        }
                    }
                }
            }
        }
    ]

    orders_cursor = order_collection.aggregate(pipeline)
    orders = await orders_cursor.to_list(length=limit)

    if not orders:
         raise HTTPException(status_code=404, detail=f"No orders found for user_id '{user_id}' with linked products.")

    next_page_url = None
    if len(orders) == limit:
        next_offset = offset + limit
        next_page_url = f"/orders/{user_id}?limit={limit}&offset={next_offset}"

    previous_page_url = None
    if offset > 0:
        previous_offset = max(0, offset - limit)
        previous_page_url = f"/orders/{user_id}?limit={limit}&offset={previous_offset}"
    
    return {
        "data": orders,
        "page": {
            "next": next_page_url,
            "limit": limit,
            "previous": previous_page_url
        }
    }