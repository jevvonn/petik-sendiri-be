from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base import get_db
from app.services.user_service import UserService
from app.schemas.user import UserRegister, UserResponse
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class EmailPasswordRequestForm:
    def __init__(
        self,
        email: str = Form(..., description="Your email address"),
        password: str = Form(..., description="Your password"),
    ):
        self.email = email
        self.password = password


@router.post("/login", response_model=Token, summary="User Login")
def login(
    db: Session = Depends(get_db),
    form_data: EmailPasswordRequestForm = Depends()
):
    """
    Login with email and password to get an access token for future requests.
    
    - **email**: Your email address
    - **password**: Your password
    """
    user = UserService.authenticate(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="User Registration")
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Valid email address
    - **full_name**: User's full name
    - **username**: Unique username
    - **password**: Password for the account
    """
    # Check if email already exists
    if UserService.get_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username already exists
    if UserService.get_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user using UserCreate schema (with defaults)
    from app.schemas.user import UserCreate
    user_create = UserCreate(
        email=user_data.email,
        full_name=user_data.full_name,
        username=user_data.username,
        password=user_data.password
    )
    
    user = UserService.create(db, user_create)
    return user
