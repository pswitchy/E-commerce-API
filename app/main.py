from fastapi import FastAPI
from .routers import products, orders

app = FastAPI()

app.include_router(products.router, tags=["Products"], prefix="/api")
app.include_router(orders.router, tags=["Orders"], prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API!"}