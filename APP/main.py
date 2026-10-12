from fastapi import FastAPI
from APP.routers.product import router as product_router

app = FastAPI(
    title="E-Commerce Backend API",
    description="Backend API for an e-commerce application",
    version="1.0.0"
)

@app.get("/")
def home():
    return{"message": "Welcome to the Ecommerce Backedn API"}

app.include_router(product_router)

