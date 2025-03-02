from typing import Optional
from pydantic import EmailStr, Field
from .base import BaseDocument

class User(BaseDocument):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    is_active: bool = True

    class Settings:
        name = "users"
