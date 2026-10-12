from fastapi import APIRouter
from fastapi import Body

router = APIRouter(
    prefix = "/products",
    tags = ["Products"]
)

products =[
    {
        "id" : 1,
        "name" : "Laptop",
        "price" : 135000,
        "quantity" : 25
    },
    {
        "id" : 2,
        "name" : "phones",
        "price" : 45000,
        "quantity" : 65
    }
]

@router.get("/")
def get_products():
    return products

@router.get("/{product_id}")
def get_prodcut(product_id : int):

    for product in products:
        if product["id"] == product_id:
            return product

    return{"message" : " product not found"}   

@router.post("/")
def create_product(product: dict = Body(...)):
    for exist_product in products:
        if exist_product["id"] == product["id"]:
            return {
                "message": "Product ID already exists"
            }

    products.append(product)

    return {
        "message": "Product successfully added",
        "product": product
    }