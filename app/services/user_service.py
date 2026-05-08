from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserResponse

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    async def register_user(self, user_create: UserCreate) -> UserResponse:
        existing_user = await self.repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        user = await self.repository.create(user_create.dict())
        return UserResponse(
            id=user["id"],
            email=user["email"],
            created_at=str(user.get("created_at"))
        )

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        from ..auth.jwt_handler import verify_password
        if not verify_password(password, user["hashed_password"]):
            return None
        return user

    async def get_user(self, user_id: str) -> Optional[UserResponse]:
        user = await self.repository.get_by_id(user_id)
        if user:
            return UserResponse(
                id=user["id"],
                email=user["email"],
                created_at=str(user.get("created_at"))
            )
        return None