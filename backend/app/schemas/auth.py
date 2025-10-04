from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import Role

# Auth schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    role: Role = Role.TEACHER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

# Preferences schemas
class UserPreferencesBase(BaseModel):
    class_mode: bool = False
    language: str = "fr"
    theme: str = "light"
    widgets_enabled: Optional[str] = None
    settings: Optional[str] = None

class UserPreferencesUpdate(BaseModel):
    class_mode: Optional[bool] = None
    language: Optional[str] = None
    theme: Optional[str] = None
    widgets_enabled: Optional[str] = None
    settings: Optional[str] = None

class UserPreferencesResponse(UserPreferencesBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
