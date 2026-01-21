"""创建数据库"""
import psycopg2
from psycopg2 import sql
import sys

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 连接到默认的postgres数据库
try:
    print("正在连接到PostgreSQL...")
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="password",
        database="postgres",
        client_encoding='utf8'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("连接成功，检查数据库是否存在...")
    # 检查数据库是否存在
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='stellar_journal'")
    exists = cursor.fetchone()
    
    if not exists:
        print("数据库不存在，正在创建...")
        # 创建数据库
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier("stellar_journal")
        ))
        print("✅ 数据库 stellar_journal 创建成功！")
    else:
        print("ℹ️  数据库 stellar_journal 已经存在")
    
    cursor.close()
    conn.close()
    print("完成！")
    
except psycopg2.OperationalError as e:
    print(f"❌ 数据库连接失败！")
    print(f"请检查：")
    print(f"1. PostgreSQL服务是否运行")
    print(f"2. 用户名是否为 'postgres'")
    print(f"3. 密码是否为 'password'")
    print(f"错误详情: {str(e)[:200]}")
except Exception as e:
    print(f"❌ 创建数据库失败: {type(e).__name__}")
    print(f"错误详情: {str(e)[:200]}")
