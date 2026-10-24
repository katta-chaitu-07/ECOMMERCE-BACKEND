from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session

from APP.schemas.Product import ProductCreate
from APP.models.product import Product
from APP.database.dependencies import get_db
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)




# GET - Get all products
@router.get("/")
def get_products(db : Session = Depends(get_db)):
    products  = db.query(Product).all()
    return products


# GET - Get a product by ID
@router.get("/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# POST - Create a new product with Pydantic validation
@router.post("/")
def create_product(
                   product: ProductCreate,
                   db : Session = Depends(get_db)
                   ):

    new_product = Product(
        id = product.id,
        name = product.name,
        price = product.price,
        quantity = product.quantity
    )

    existing_product = db.query(Product).filter(
                       Product.id == product.id
                ).first()

    if existing_product :

        raise HTTPException(
            status_code = 409,
            detail = "product ID is already exists "
        )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return{
        "message" : "Product is successfully added",
        "product" : new_product
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

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


# PUT - Replace an entire product with Pydantic validation
@router.put("/{product_id}")
def replace_product(
    product_id: int,
    updated_product: ProductCreate
):

    for index, product in enumerate(products):

        if product["id"] == product_id:

            if updated_product.id != product_id:
                raise HTTPException(
                    status_code=400,
                    detail="Product ID mismatch"
                )

            products[index] = updated_product.model_dump()

            return {
                "message": "Product is successfully updated",
                "product": products[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


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

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )