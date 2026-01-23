"""
删除测试用户脚本
"""
from app.core.database import SessionLocal
from app.models.user import User

def delete_test_users():
    """删除指定的测试用户"""
    db = SessionLocal()
    
    try:
        # 要删除的测试邮箱列表
        test_emails = [
            "yaoc_0309@163.com",
            "chenyao@163.com",
            "chenyao@zerozero.cn"
        ]
        
        deleted_count = 0
        
        for email in test_emails:
            user = db.query(User).filter(User.email == email).first()
            if user:
                db.delete(user)
                deleted_count += 1
                print(f"✅ 已删除用户: {email}")
            else:
                print(f"⚠️  未找到用户: {email}")
        
        if deleted_count > 0:
            db.commit()
            print(f"\n🎉 成功删除 {deleted_count} 个测试用户")
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
