from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')

class UserUpdateDTO(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
