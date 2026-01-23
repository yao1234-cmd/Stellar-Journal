"""创建临时用户"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from app.core.database import SessionLocal
from app.models.user import User
import uuid

# 临时用户ID
TEMP_USER_ID = "00000000-0000-0000-0000-000000000001"

try:
    print("正在创建临时用户...")
    
    db = SessionLocal()
    
    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.id == TEMP_USER_ID).first()
    
    if existing_user:
        print("ℹ️  临时用户已存在")
    else:
        # 创建临时用户
        temp_user = User(
            id=TEMP_USER_ID,
            email="temp@stellar.journal",
            username="temp_user",
            hashed_password="not_used"  # 临时用户不需要密码
        )
        
        db.add(temp_user)
        db.commit()
        print("✅ 临时用户创建成功！")
        print(f"   用户ID: {TEMP_USER_ID}")
        print(f"   邮箱: temp@stellar.journal")
    
    db.close()
    print("\n完成！现在可以创建记录了。")
    
except Exception as e:
    print(f"❌ 创建失败: {type(e).__name__}")
    print(f"错误详情: {str(e)[:200]}")
