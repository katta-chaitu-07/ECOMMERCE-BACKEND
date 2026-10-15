from fastapi import APIRouter, Body
from APP.schemas.Product import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 135000,
        "quantity": 25
    },
    {
        "id": 2,
        "name": "phones",
        "price": 45000,
        "quantity": 65
    }
]


# GET - Get all products
@router.get("/")
def get_products():
    return products


# GET - Get a product by ID
@router.get("/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product

    return {
        "message": "Product not found"
    }


# POST - Create a new product with Pydantic validation
@router.post("/")
def create_product(product: ProductCreate):

    new_product = product.model_dump()

    for exist_product in products:
        if exist_product["id"] == new_product["id"]:
            return {
                "message": "Product ID already exists"
            }

    products.append(new_product)

    return {
        "message": "Product successfully added",
        "product": new_product
    }


# PATCH - Update specific fields of a product
@router.patch("/{product_id}")
def update_product(
    product_id: int,
    updated_data: dict = Body(...)
):
    for product in products:
        if product["id"] == product_id:
            product.update(updated_data)

            return {
                "message": "Product is updated",
                "product": product
            }

    return {
        "message": "Product not found"
    }


# PUT - Replace an entire product with Pydantic validation
@router.put("/{product_id}")
def replace_product(
    product_id: int,
    updated_product: ProductCreate
):
    for index, product in enumerate(products):

        if product["id"] == product_id:

            if updated_product.id != product_id:
                return {
                    "message": "Product ID is mismatched"
                }

            products[index] = updated_product.model_dump()

            return {
                "message": "Product is successfully updated",
                "product": products[index]
            }

    return {
        "message": "Product not found"
    }


# DELETE - Delete a product
@router.delete("/{product_id}")
def delete_product(product_id: int):

    for index, product in enumerate(products):
        if product["id"] == product_id:

            deleted_product = products.pop(index)

            return {
                "message": "Product is successfully deleted",
                "product": deleted_product
            }

    return {
        "message": "Product not found"
    }