"""
Records API - 记录相关接口
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.core.deps import get_current_verified_user
from app.models.user import User
from app.models.record import Record, RecordType
from app.schemas.record import RecordCreate, RecordResponse, RecordListResponse
from app.services.emotion_service import emotion_service
from app.services.whisper_service import whisper_service
from app.services.planet_service import planet_service

router = APIRouter()


@router.options("/")
async def options_records():
    """处理 OPTIONS 预检请求"""
    return {"status": "ok"}


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
    record_data: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    创建记录（需要认证且邮箱已验证）
    
    - **type**: 记录类型 (mood/spark/thought)
    - **content**: 记录内容
    """
    try:
        # 创建记录对象
        new_record = Record(
            user_id=str(current_user.id),
            type=RecordType[record_data.type.value.upper()],
            content=record_data.content,
            audio_url=record_data.audio_url
        )
        
        # 根据类型进行不同的处理
        if record_data.type == "mood":
            # 心情：AI情感分析
            emotion_result = await emotion_service.analyze_emotion(record_data.content)
            new_record.emotion_analysis = emotion_result
            
            # 映射颜色
            color = emotion_service.emotion_to_color(
                emotion_result["valence"],
                emotion_result["arousal"]
            )
            new_record.color_hex = color
            
        elif record_data.type == "spark":
            # 灵感：提取关键词 + 计算位置
            # 简化版：从内容中提取关键词（实际可用更复杂的NLP）
            words = record_data.content.split()[:3]
            new_record.keywords = words
            
            # 计算星星位置
            # 查询已有星星数量
            spark_count = db.query(Record).filter(
                Record.user_id == str(current_user.id),
                Record.type == RecordType.SPARK
            ).count()
            
            # 使用当前时间而不是 created_at（因为此时还是None）
            from datetime import datetime
            position = planet_service.calculate_star_position(
                spark_count,
                spark_count + 1,
                datetime.now()
            )
            new_record.position_data = position
            
        elif record_data.type == "thought":
            # 思考：提取主题（简化版）
            new_record.theme_cluster = "日常思考"  # 实际应该用聚类算法
            new_record.keywords = record_data.content.split()[:5]
            
            # 计算树的位置
            position = planet_service.calculate_tree_position(
                new_record.theme_cluster,
                0
            )
            new_record.position_data = position
        
        # 保存到数据库
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        return new_record
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建记录失败: {str(e)}"
        )


@router.get("/", response_model=RecordListResponse)
async def get_records(
    skip: int = 0,
    limit: int = 50,
    record_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    获取记录列表（需要认证且邮箱已验证）
    
    - **skip**: 跳过数量
    - **limit**: 返回数量
    - **record_type**: 记录类型筛选 (mood/spark/thought)
    """
    query = db.query(Record).filter(Record.user_id == str(current_user.id))
    
    if record_type:
        try:
            query = query.filter(Record.type == RecordType[record_type.upper()])
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"无效的记录类型: {record_type}"
            )
    
    total = query.count()
    records = query.order_by(Record.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "records": records,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit
    }


@router.get("/history")
async def get_record_history(
    days: int = 30,
    record_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """
    获取历史记录（需要认证且邮箱已验证）
    
    - **days**: 获取最近多少天的记录（默认30天）
    - **record_type**: 筛选记录类型 (mood/spark/thought)，不传则返回所有
    """
    try:
        from datetime import datetime, timedelta
        
        # 计算开始日期
        start_date = datetime.now() - timedelta(days=days)
        
        # 构建查询
        query = db.query(Record).filter(
            Record.user_id == current_user.id,
            Record.created_at >= start_date
        )
        
        # 类型筛选
        if record_type:
            query = query.filter(Record.type == record_type)
        
        # 按时间倒序排列
        records = query.order_by(Record.created_at.desc()).all()
        
        # 转换为响应格式
        result = []
        for record in records:
            item = {
                "id": str(record.id),
                "type": record.type.value,
                "content": record.content,
                "created_at": record.created_at.isoformat(),
            }
            
            # 根据类型添加额外字段
            if record.type == RecordType.MOOD and record.emotion_analysis:
                item["emotion"] = record.emotion_analysis
            elif record.type == RecordType.SPARK and record.keywords:
                item["keywords"] = record.keywords
            elif record.type == RecordType.THOUGHT and record.theme_cluster:
                item["theme"] = record.theme_cluster
            
            result.append(item)
        
        print(f"✅ 成功返回 {len(result)} 条记录")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 获取历史记录失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取历史记录失败: {str(e)}"
        )


@router.get("/{record_id}", response_model=RecordResponse)
async def get_record(
    record_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """获取单条记录详情（需要认证且邮箱已验证）"""
    try:
        record_uuid = uuid.UUID(record_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的记录ID格式"
        )
    
    record = db.query(Record).filter(
        Record.id == record_uuid,
        Record.user_id == str(current_user.id)
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记录不存在"
        )
    
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_record(
    record_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_verified_user)
):
    """删除记录（需要认证且邮箱已验证）"""
    try:
        record_uuid = uuid.UUID(record_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的记录ID格式"
        )
    
    record = db.query(Record).filter(
        Record.id == record_uuid,
        Record.user_id == str(current_user.id)
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记录不存在"
        )
    
    db.delete(record)
    db.commit()
    
    return None


@router.post("/transcribe", response_model=dict)
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    语音转文字
    
    上传音频文件，返回转写文本
    """
    try:
        # 检查文件格式
        file_ext = audio.filename.split(".")[-1].lower()
        if file_ext not in ["mp3", "wav", "m4a", "ogg"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的音频格式: {file_ext}"
            )
        
        # 读取文件内容
        content = await audio.read()
        
        # 检查文件大小（10MB限制）
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件大小超过10MB限制"
            )
        
        # 调用Whisper服务
        text = await whisper_service.transcribe(audio.file)
        
        return {
            "text": text,
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"语音转写失败: {str(e)}"
        )
