
from fastapi import FastAPI

from APP.routers.product import router as product_router
from APP.routers.user import router as user_router
from APP.routers import cart
from APP.routers.order import router as order_router


app = FastAPI(
    title="E-Commerce Backend API",
    description="Backend API for an e-commerce application",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the E-Commerce Backend API"
    }


# Register API routers
app.include_router(product_router)
app.include_router(user_router)
app.include_router(cart.router)
app.include_router(order_router)
