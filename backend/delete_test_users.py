"""
删除测试用户脚本
"""
import os
from app.core.database import SessionLocal
from app.models.user import User

def delete_test_users():
    """删除指定的测试用户"""
    db = SessionLocal()
    
    try:
        # 从环境变量加载测试邮箱列表，或使用非 PII 占位符
        test_emails_env = os.environ.get("TEST_USER_EMAILS", "")
        
        if test_emails_env:
            # 从环境变量解析邮箱列表（逗号分隔）
            test_emails = [email.strip() for email in test_emails_env.split(",") if email.strip()]
        else:
            # 使用确定性的非 PII 占位符
            test_emails = [
                "test_user_1@example.test",
                "test_user_2@example.test",
                "test_user_3@example.test"
            ]
        
        # 验证：确保没有使用真实邮箱
        for email in test_emails:
            if not (email.endswith("@example.test") or email.endswith("@test.local")):
                # 无论来源如何，非测试域名都应该报错并停止
                print(f"❌ 错误: 邮箱 {email} 不是有效的测试邮箱域名")
                print(f"   只允许删除以 @example.test 或 @test.local 结尾的邮箱")
                print(f"   来源: {'环境变量 TEST_USER_EMAILS' if test_emails_env else '默认配置'}")
                return  # 提前返回，避免触发外层异常处理
        
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
