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


# to add the item 
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

# patch (for updating a specific column of a item )
@router.patch("/{product_id}")
def update_product(product_id : int, updated_data : dict = Body(...)):
    for product in products:
        if product["id"] == product_id:
            product.update(updated_data)

            return{ "message" : "product is updated",
                    "product" : product
                   }

    return{"message" : "product  not found "}


# put (replace the entire item )
@router.put("/{product_id}")
def replace_product(product_id: int, updated_product: dict):

    for index, product in enumerate(products):

        if product["id"] == product_id:

            if updated_product["id"] != product_id:
                return {"message": "product id does not change"}

            products[index] = updated_product

            return {
                "message": "product is successfully updated",
                "product": updated_product
            }

    return {
        "message": "product not found"
    }

# delete method (delete the item from the products)
@router.delete("/{product_id}")
def delete_product(product_id : int):

    for index,product in enumerate(products):

        if product["id"] == product_id :

            deleted_product = products.pop(index)    

            return{
                "message" : "product is successfully deleted",
                "product" : deleted_product
            }

    return{
        "message" : "product not found "
    }    