"""检查数据库中的记录数量"""
from app.models.record import Record
from app.core.database import SessionLocal

db = SessionLocal()
try:
    count = db.query(Record).count()
    print(f"数据库中有 {count} 条记录")
    
    # 显示最近的5条记录
    records = db.query(Record).order_by(Record.created_at.desc()).limit(5).all()
    print(f"\n最近的记录：")
    for record in records:
        print(f"  - {record.type.value}: {record.content[:30]}... (创建于: {record.created_at})")
finally:
    db.close()
