"""初始化数据库"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database
from app.core.config import settings
from app.core.database import Base
from app.models import record, user

try:
    print("正在检查数据库...")
    
    # 检查数据库是否存在，如果不存在则创建
    if not database_exists(settings.DATABASE_URL):
        print("数据库不存在，正在创建...")
        create_database(settings.DATABASE_URL)
        print("✅ 数据库创建成功！")
    else:
        print("ℹ️  数据库已存在")
    
    # 创建所有表
    print("正在创建数据库表...")
    from app.core.database import engine
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功！")
    
    print("\n数据库初始化完成！")
    
except Exception as e:
    print(f"❌ 初始化失败: {type(e).__name__}")
    print(f"如果是连接错误，请检查：")
    print(f"1. PostgreSQL是否运行")
    print(f"2. 用户名密码是否正确")
    print(f"3. 在 app/core/config.py 中的 DATABASE_URL")
