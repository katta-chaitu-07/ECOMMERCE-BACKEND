from fastapi import APIRouter , Depends, status , HTTPException

from APP.security.dependencies import get_current_user

from sqlalchemy.orm import Session

from APP.database.dependencies import get_db
from APP.models.user import User
from APP.schemas.User import UserCreate, UserResponse , UserLogin

from APP.security.password import hash_password,verify_password
from APP.security.jwt import create_access_token


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/register",response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def register_user(user_data : UserCreate , db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()


    if existing_user :

        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )

    hashed_password = hash_password(user_data.password)    

    new_user = User(

        name = user_data.name,

        email = user_data.email,

        password_hash = hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user 

@router.post("/login")
def login_user(user_data : UserLogin , db : Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == user_data.email
    ).first()


    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "  Invalid user and password "
        ) 


    from fastapi import APIRouter , Depends, status , HTTPException

from sqlalchemy.orm import Session

from APP.database.dependencies import get_db
from APP.models.user import User
from APP.schemas.User import UserCreate, UserResponse , UserLogin

from APP.security.password import hash_password,verify_password
from APP.security.jwt import create_access_token


router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/register",response_model = UserResponse, status_code = status.HTTP_201_CREATED)
def register_user(user_data : UserCreate , db : Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()


    if existing_user :

        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered"
        )

    hashed_password = hash_password(user_data.password)    

    new_user = User(

        name = user_data.name,

        email = user_data.email,

        password_hash = hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user 

@router.post("/login")
def login_user(user_data : UserLogin , db : Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == user_data.email
    ).first()


    if not user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "  Invalid user and password "
        ) 


    access_token = create_access_token(
           
           data={"user_id": user.id}
           )

    return {
    "access_token": access_token,
    "token_type": "bearer"
     }    

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user

    
        

    
    