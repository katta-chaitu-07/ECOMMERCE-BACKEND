from pydantic import BaseModel , EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):

    name : str = Field(min_length = 2, max_length = 50)

    email : EmailStr

    password : str = Field(min_lenght = 8)


class UserResponse(BaseModel):

    id : int

    name : str

    email : EmailStr

    is_active : bool

    created_at : datetime

    model_config = {
        "from_attributes" : True
    }    


class UserLogin(BaseModel):

    email :EmailStr

    password : str    