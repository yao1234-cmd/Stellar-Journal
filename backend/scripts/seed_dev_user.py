"""
开发环境种子脚本 - 创建测试用户

此脚本用于在开发/测试环境中创建测试用户
不应在生产环境中运行

使用方法:
    python backend/scripts/seed_dev_user.py
"""
import sys
import os

# 确保可以导入 app 模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def seed_dev_user():
    """创建开发环境测试用户"""
    
    # 环境检查
    app_env = os.environ.get("ENVIRONMENT", "development")
    if app_env == "production":
        print("❌ 错误: 此脚本不应在生产环境运行")
        print("   当前环境: ENVIRONMENT=production")
        return False
    
    db = SessionLocal()
    
    try:
        # 测试用户配置
        test_user_id = "00000000-0000-0000-0000-000000000001"
        test_email = "dev@example.test"
        test_username = "dev_user"
        test_password = "dev123456"  # 开发环境测试密码
        
        print(f"开始创建测试用户...")
        print(f"环境: {app_env}")
        
        # 检查用户是否已存在
        existing_user = db.query(User).filter(User.id == test_user_id).first()
        
        if existing_user:
            print(f"ℹ️  测试用户已存在")
            print(f"   ID: {test_user_id}")
            print(f"   邮箱: {existing_user.email}")
            print(f"   用户名: {existing_user.username}")
            return True
        
        # 创建新的测试用户
        hashed_password = get_password_hash(test_password)
        test_user = User(
            id=test_user_id,
            email=test_email,
            username=test_username,
            hashed_password=hashed_password,
            is_active=True,
            is_email_verified=True  # 开发环境默认已验证
        )
        
        db.add(test_user)
        db.commit()
        
        print("✅ 测试用户创建成功！")
        print(f"   ID: {test_user_id}")
        print(f"   邮箱: {test_email}")
        print(f"   用户名: {test_username}")
        print(f"   密码: {test_password}")
        print(f"   已激活: True")
        print(f"   邮箱已验证: True")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ 创建失败: {type(e).__name__}")
        print(f"   错误详情: {str(e)}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("开发环境种子脚本 - 创建测试用户")
    print("=" * 60)
    print()
    
    success = seed_dev_user()
    
    print()
    if success:
        print("🎉 完成！你现在可以使用测试用户登录了")
    else:
        print("⚠️  脚本执行遇到问题，请检查错误信息")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
