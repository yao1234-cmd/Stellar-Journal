"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
import logging

logger = logging.getLogger(__name__)
from app.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    decode_token,
    generate_verification_token
)
from app.core.deps import get_current_user, get_current_verified_user
from app.models.user import User
from app.schemas.auth import (
    UserRegister, 
    UserLogin, 
    Token, 
    EmailVerification,
    UserResponse,
    MessageResponse,
    ResendVerificationRequest
)
from app.services.email_service import email_service

router = APIRouter()


@router.options("/{full_path:path}")
async def options_handler():
    """处理所有 OPTIONS 预检请求"""
    return {"status": "ok"}


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user and send verification email
    """
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # Check if email exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # Generate verification token
    verification_token = generate_verification_token()
    verification_expires = datetime.now(timezone.utc) + timedelta(hours=24)
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_email_verified=False,
        verification_token=verification_token,
        verification_token_expires=verification_expires
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Send verification email
    email_sent = await email_service.send_verification_email(
        email=user.email,
        username=user.username,
        token=verification_token
    )
    
    if not email_sent:
        # Don't fail registration if email fails, user can request resend
        logger.warning("Failed to send verification email to user")
    else:
        logger.info("Verification email sent successfully")
    
    return MessageResponse(message="注册成功！请检查您的邮箱以验证账号")


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(verification: EmailVerification, db: Session = Depends(get_db)):
    """
    Verify user email with token
    """
    # First, let's check if any user has this token (regardless of verification status)
    user_any = db.query(User).filter(User.verification_token == verification.token).first()
    
    # If user_any is found but already verified, this is a duplicate request (React StrictMode)
    if user_any and user_any.is_email_verified:
        return MessageResponse(message="邮箱验证成功！您现在可以登录了")
    
    # Now the original query
    user = db.query(User).filter(
        User.verification_token == verification.token,
        User.is_email_verified == False
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的验证链接"
        )
    
    # Check if token expired
    if user.verification_token_expires and user.verification_token_expires < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证链接已过期，请重新注册或请求新的验证邮件"
        )
    
    # Mark email as verified
    user.is_email_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    
    db.commit()
    
    return MessageResponse(message="邮箱验证成功！您现在可以登录了")


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请先验证您的邮箱"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的 refresh token"
    )
    
    # Decode refresh token
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id_str).first()
    if not user or not user.is_active:
        raise credentials_exception
    
    # Create new tokens
    new_access_token = create_access_token(data={"sub": str(user.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    return current_user


@router.post("/resend-verification", response_model=MessageResponse)
async def resend_verification_email(
    payload: ResendVerificationRequest, 
    db: Session = Depends(get_db)
):
    """
    Resend verification email
    """
    user = db.query(User).filter(
        User.email == payload.email,
        User.is_email_verified == False
    ).first()
    
    if not user:
        # Don't reveal if email exists or not
        return MessageResponse(message="如果该邮箱存在且未验证，验证邮件已发送")
    
    # Generate new token
    verification_token = generate_verification_token()
    verification_expires = datetime.now(timezone.utc) + timedelta(hours=24)
    
    user.verification_token = verification_token
    user.verification_token_expires = verification_expires
    db.commit()
    
    # Send email
    try:
        email_sent = await email_service.send_verification_email(
            email=user.email,
            username=user.username,
            token=verification_token
        )
        
        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="发送验证邮件失败，请稍后重试"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to send verification email: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="发送验证邮件失败，请稍后重试"
        )
    
    return MessageResponse(message="验证邮件已发送")
