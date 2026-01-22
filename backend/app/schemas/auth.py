"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import uuid


class UserRegister(BaseModel):
    """User registration schema"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v):
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("用户名只能包含字母、数字、下划线和连字符")
        return v
    
    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("密码长度至少为 8 个字符")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含至少一个数字")
        if not any(c.isalpha() for c in v):
            raise ValueError("密码必须包含至少一个字母")
        return v


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: str  # user_id
    exp: int
    type: str  # "access" or "refresh"


class EmailVerification(BaseModel):
    """Email verification schema"""
    token: str


class UserResponse(BaseModel):
    """User response schema"""
    id: uuid.UUID
    username: str
    email: str
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
