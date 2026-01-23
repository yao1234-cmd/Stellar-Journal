"""
删除测试用户脚本
"""
import os
from app.core.database import SessionLocal
from app.models.user import User

def delete_test_users():
    """删除指定的用户"""
    db = SessionLocal()
    
    try:
        # 从环境变量加载邮箱列表
        test_emails_env = os.environ.get("TEST_USER_EMAILS", "")
        
        if test_emails_env:
            # 从环境变量解析邮箱列表（逗号分隔）
            test_emails = [email.strip() for email in test_emails_env.split(",") if email.strip()]
        else:
            # 默认要删除的邮箱列表
            test_emails = [
                "chenyao@zerozero.cn"
            ]
        
        # 显示将要删除的用户
        print(f"将要删除以下邮箱的用户:")
        for email in test_emails:
            print(f"  - {email}")
        
        # 确认操作
        confirm = input(f"\n⚠️  确认删除这 {len(test_emails)} 个用户? (输入 'yes' 确认): ")
        
        if confirm.lower() != 'yes':
            print("❌ 取消删除操作")
            return
        
        deleted_count = 0
        
        for email in test_emails:
            user = db.query(User).filter(User.email == email).first()
            if user:
                print(f"删除用户: {user.username} ({email})")
                db.delete(user)
                deleted_count += 1
                print(f"✅ 已删除用户: {email}")
            else:
                print(f"⚠️  未找到用户: {email}")
        
        if deleted_count > 0:
            db.commit()
            print(f"\n🎉 成功删除 {deleted_count} 个用户")
        else:
            print("\n❌ 没有找到需要删除的用户")
            
    except Exception as e:
        db.rollback()
        print(f"❌ 删除失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("开始删除测试用户...\n")
    delete_test_users()
