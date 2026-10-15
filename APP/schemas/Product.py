from pydantic import BaseModel,Field

class ProductCreate(BaseModel):

    name : str = Field(min_length = 2)

    price : float = Field(gt = 0) 

    quantity : int = Field(ge=0)
