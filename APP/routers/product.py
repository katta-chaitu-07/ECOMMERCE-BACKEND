
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from APP.schemas.Product import (
    ProductCreate,
    ProductUpdate
)
from APP.models.product import Product
from APP.database.dependencies import get_db


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# ----------------------------------------
# Helper: Format Product Response
# ----------------------------------------

def format_product(product):

    return {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
        "image_url": product.image_url
    }


# ----------------------------------------
# GET - Get all products
# ----------------------------------------

@router.get("/")
def get_products(db: Session = Depends(get_db)):

    products = db.query(Product).all()

    return [
        format_product(product)
        for product in products
    ]


# ----------------------------------------
# GET - Get product by ID
# ----------------------------------------

@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return format_product(product)


# ----------------------------------------
# POST - Create a new product
# ----------------------------------------

@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):

    existing_product = db.query(Product).filter(
        Product.id == product.id
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail="Product ID already exists"
        )

    new_product = Product(
        id=product.id,
        name=product.name,
        price=product.price,
        quantity=product.quantity,
        image_url=product.image_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product successfully added",
        "product": format_product(new_product)
    }


# ----------------------------------------
# PATCH - Update selected product fields
# ----------------------------------------

@router.patch("/{product_id}")
def update_product(
    product_id: int,
    updated_data: ProductUpdate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_fields = updated_data.model_dump(
        exclude_unset=True
    )

    if not update_fields:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    # Name, price and quantity cannot be null
    for field, value in update_fields.items():

        if value is None and field != "image_url":
            raise HTTPException(
                status_code=400,
                detail=f"{field} cannot be null"
            )

    for field, value in update_fields.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return {
        "message": "Product successfully updated",
        "product": format_product(product)
    }


# ----------------------------------------
# PUT - Replace an entire product
# ----------------------------------------

@router.put("/{product_id}")
def replace_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if updated_product.id != product_id:
        raise HTTPException(
            status_code=400,
            detail="Product ID mismatch"
        )

    product.name = updated_product.name
    product.price = updated_product.price
    product.quantity = updated_product.quantity
    product.image_url = updated_product.image_url

    db.commit()
    db.refresh(product)

    return {
        "message": "Product successfully replaced",
        "product": format_product(product)
    }


# ----------------------------------------
# DELETE - Delete a product
# ----------------------------------------

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    deleted_product = format_product(product)

    db.delete(product)
    db.commit()

    return {
        "message": "Product successfully deleted",
        "product": deleted_product
    }
