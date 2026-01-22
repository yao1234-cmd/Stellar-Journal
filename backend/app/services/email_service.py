"""
Email service using Resend
"""
import resend
from typing import Optional
from app.core.config import settings


class EmailService:
    """Email service for sending verification and notification emails"""
    
    def __init__(self):
        if settings.RESEND_API_KEY:
            resend.api_key = settings.RESEND_API_KEY
    
    async def send_verification_email(self, email: str, username: str, token: str) -> bool:
        """Send email verification link"""
        try:
            verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center;">
                    <h1 style="color: white; margin: 0;">✨ 欢迎加入 Stellar Journal</h1>
                </div>
                
                <div style="padding: 30px; background: #f9fafb; border-radius: 10px; margin-top: 20px;">
                    <p style="font-size: 16px; color: #374151;">嗨 {username}，</p>
                    
                    <p style="font-size: 16px; color: #374151; line-height: 1.6;">
                        感谢您注册 Stellar Journal！这是一个记录您情感星球的空间 🌍
                    </p>
                    
                    <p style="font-size: 16px; color: #374151; line-height: 1.6;">
                        请点击下方按钮验证您的邮箱地址：
                    </p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{verification_url}" 
                           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  color: white; 
                                  padding: 15px 40px; 
                                  text-decoration: none; 
                                  border-radius: 25px; 
                                  font-size: 16px; 
                                  display: inline-block;">
                            验证邮箱
                        </a>
                    </div>
                    
                    <p style="font-size: 14px; color: #6b7280;">
                        如果按钮无法点击，请复制以下链接到浏览器：<br>
                        <a href="{verification_url}" style="color: #667eea; word-break: break-all;">{verification_url}</a>
                    </p>
                    
                    <p style="font-size: 14px; color: #6b7280; margin-top: 20px;">
                        此链接将在 24 小时后失效。
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; color: #9ca3af; font-size: 12px;">
                    <p>如果您没有注册此账号，请忽略此邮件。</p>
                    <p>© 2026 Stellar Journal. All rights reserved.</p>
                </div>
            </body>
            </html>
            """
            
            params = {
                "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
                "to": [email],
                "subject": "验证您的 Stellar Journal 邮箱",
                "html": html_content,
            }
            
            # Send email
            response = resend.Emails.send(params)
            return True
            
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            return False
    
    async def send_password_reset_email(self, email: str, username: str, token: str) -> bool:
        """Send password reset link (for future use)"""
        try:
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center;">
                    <h1 style="color: white; margin: 0;">🔒 重置密码</h1>
                </div>
                
                <div style="padding: 30px; background: #f9fafb; border-radius: 10px; margin-top: 20px;">
                    <p style="font-size: 16px; color: #374151;">嗨 {username}，</p>
                    
                    <p style="font-size: 16px; color: #374151; line-height: 1.6;">
                        我们收到了您的密码重置请求。
                    </p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  color: white; 
                                  padding: 15px 40px; 
                                  text-decoration: none; 
                                  border-radius: 25px; 
                                  font-size: 16px; 
                                  display: inline-block;">
                            重置密码
                        </a>
                    </div>
                    
                    <p style="font-size: 14px; color: #6b7280;">
                        此链接将在 1 小时后失效。
                    </p>
                </div>
                
                <div style="text-align: center; padding: 20px; color: #9ca3af; font-size: 12px;">
                    <p>如果您没有请求重置密码，请忽略此邮件。</p>
                    <p>© 2026 Stellar Journal. All rights reserved.</p>
                </div>
            </body>
            </html>
            """
            
            params = {
                "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>",
                "to": [email],
                "subject": "重置您的 Stellar Journal 密码",
                "html": html_content,
            }
            
            response = resend.Emails.send(params)
            return True
            
        except Exception as e:
            print(f"Failed to send password reset email: {e}")
            return False


email_service = EmailService()
