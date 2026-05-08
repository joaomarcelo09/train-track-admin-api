from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ..services.user_service import UserService
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token
from ..auth.jwt_handler import create_access_token, get_current_user
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    service = UserService()
    return await service.register_user(user_data)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    service = UserService()
    user = await service.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        created_at=str(current_user.get("created_at"))
    )