from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# 直接使用配置中的数据库 URL，绕过 Settings 验证
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/stellar_journal"

def check_db():
    print("尝试连接数据库...")
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        print("连接成功，尝试执行查询...")
        # 尝试简单的查询
        result = db.execute(text("SELECT 1")).scalar()
        print(f"查询结果: {result}")
        
        # 尝试查询 records 表
        print("尝试查询 records 表数量...")
        count = db.execute(text("SELECT COUNT(*) FROM records")).scalar()
        print(f"Records 表记录数: {count}")
        
        db.close()
        print("测试完成，数据库连接正常。")
        return True
    except Exception as e:
        print(f"❌ 数据库连接或查询失败: {e}")
        return False

if __name__ == "__main__":
    success = check_db()
    if not success:
        sys.exit(1)
