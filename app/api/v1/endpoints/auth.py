from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.base import get_db
from app.services.user_service import UserService
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
