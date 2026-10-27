
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
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


# GET - Get a product by ID
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

    return product


# POST - Create a new product
@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    # Check whether the product ID already exists
    existing_product = db.query(Product).filter(
        Product.id == product.id
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail="Product ID already exists"
        )

    # Create a new database object
    new_product = Product(
        id=product.id,
        name=product.name,
        price=product.price,
        quantity=product.quantity
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product is successfully added",
        "product": {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
            "quantity": new_product.quantity
        }
    }


# PATCH - Update specific fields of a product
@router.patch("/{product_id}")
def update_product(
    product_id: int,
    updated_data: dict = Body(...),
    db: Session = Depends(get_db)
):
    # Find the existing product
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Allow only these fields to be updated
    allowed_fields = {"name", "price", "quantity"}

    # Reject unsupported fields
    invalid_fields = set(updated_data.keys()) - allowed_fields

    if invalid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid fields: {', '.join(sorted(invalid_fields))}"
        )

    # Update only the fields provided
    for field, value in updated_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return {
        "message": "Product is updated",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }
    }


# PUT - Replace an entire product
@router.put("/{product_id}")
def replace_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    # Find the existing product
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Ensure the body ID matches the URL ID
    if updated_product.id != product_id:
        raise HTTPException(
            status_code=400,
            detail="Product ID mismatch"
        )

    # Replace all editable product fields
    product.name = updated_product.name
    product.price = updated_product.price
    product.quantity = updated_product.quantity

    db.commit()
    db.refresh(product)

    return {
        "message": "Product is successfully updated",
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }
    }


# DELETE - Delete a product
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    # Find the existing product
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Store the details before deletion
    deleted_product = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

    db.delete(product)
    db.commit()

    return {
        "message": "Product is successfully deleted",
        "product": deleted_product
    }
