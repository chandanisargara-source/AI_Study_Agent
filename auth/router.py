from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User
from schemas.user_schema import UserCreate, UserLogin
from services.security import hash_password, verify_password
from auth.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already exists"
        }

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful",
        "user_id": new_user.id
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return {
            "message": "User not found"
        }

    if not verify_password(
        user.password,
        existing_user.password
    ):
        return {
            "message": "Wrong password"
        }


    token = create_access_token(
        {
            "user_id": existing_user.id,
            "email": existing_user.email,
            "role": existing_user.role
        }
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }