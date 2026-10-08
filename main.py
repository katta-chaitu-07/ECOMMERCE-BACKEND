# import statement 
from fastapi import FastAPI

# creating the FastAPI() application
app = FastAPI()

# python list contains the prouducts 
products = [
    {
        "id" : 1,
        "name" : "Laptop",
        "price" : 50000,
        "quantity" : 10
    },

    {
        "id" : 2,
        "name" : "phone",
        "price" : 25000,
        "quantity" : 15
    }
]

@app.get("/products")
def get_products():
    return products
