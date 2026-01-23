# API 接口文档 📡

Base URL: `http://localhost:8000/api/v1`

## 认证

当前版本使用临时用户ID，未实现完整认证系统。

## Records API

### 创建记录

**请求**
```http
POST /records/
Content-Type: application/json

{
  "type": "mood",  // "mood" | "spark" | "thought"
  "content": "今天心情很好！",
  "audio_url": null  // 可选
}
```

**响应**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "type": "mood",
  "content": "今天心情很好！",
  "emotion_analysis": {
    "valence": 0.85,
    "arousal": 0.6,
    "primary_emotion": "joy",
    "emotion_scores": {
      "joy": 0.9,
      "calm": 0.5,
      "anxiety": 0.1
    }
  },
  "color_hex": "#FFD700",
  "position_data": null,
  "created_at": "2024-05-15T10:30:00Z"
}
```

### 获取记录列表

**请求**
```http
GET /records/?skip=0&limit=50&record_type=mood
```

**响应**
```json
{
  "records": [...],
  "total": 100,
  "page": 1,
  "page_size": 50
}
```

### 获取单条记录

**请求**
```http
GET /records/{record_id}
```

### 删除记录

**请求**
```http
DELETE /records/{record_id}
```

**响应**
```
204 No Content
```

### 语音转文字

**请求**
```http
POST /records/transcribe
Content-Type: multipart/form-data

audio: <file>
```

**响应**
```json
{
  "text": "转写的文字内容",
  "success": true
}
```

## Planet API

### 获取星球状态

**请求**
```http
GET /planet/state?target_date=2024-05-15
```

**响应**
```json
{
  "date": "2024-05-15",
  "atmosphere_color": "#87CEEB",
  "stars": [
    {
      "id": "uuid",
      "position": {
        "x": 2.0,
        "y": 0.1,
        "z": 1.5,
        "orbit_radius": 2.5,
        "orbit_angle": 45
      },
      "color": "#FFD700",
      "size": 0.1,
      "keyword": "创意"
    }
  ],
  "trees": [
    {
      "id": "tree-theme",
      "position": {"x": 0.5, "y": 0.8, "z": 0.3},
      "theme": "工作思考",
      "leaf_count": 5,
      "size": 0.5
    }
  ],
  "total_records": 12
}
```

### 获取历史数据

**请求**
```http
GET /planet/history?days=30
```

**响应**
```json
{
  "history": [
    {
      "date": "2024-05-01",
      "atmosphere_color": "#A5B4FC",
      "record_count": 3
    },
    ...
  ],
  "start_date": "2024-04-15",
  "end_date": "2024-05-15"
}
```

### 获取统计信息

**请求**
```http
GET /planet/stats
```

**响应**
```json
{
  "total_records": 150,
  "mood_count": 60,
  "spark_count": 45,
  "thought_count": 45,
  "start_date": "2024-01-01",
  "days_active": 135
}
```

## 错误响应

所有错误响应遵循统一格式：

```json
{
  "detail": "错误描述信息"
}
```

### 常见状态码

- `200` OK - 请求成功
- `201` Created - 资源创建成功
- `204` No Content - 删除成功
- `400` Bad Request - 请求参数错误
- `404` Not Found - 资源不存在
- `500` Internal Server Error - 服务器错误

## 限流

当前版本未实现限流，生产环境应添加。

## 完整文档

访问 http://localhost:8000/docs 查看交互式 API 文档（Swagger UI）
