"""
Emotion Analysis Service - 情感分析服务
支持 OpenAI 和智谱 AI 进行情感分析并映射到颜色
"""
from typing import Dict, Tuple
import openai
from zhipuai import ZhipuAI
from app.core.config import settings
import json
import colorsys
import math


class EmotionService:
    """情感分析服务"""
    
    def __init__(self):
        self.ai_provider = settings.AI_PROVIDER.lower()
        
        if self.ai_provider == "openai":
            openai.api_key = settings.OPENAI_API_KEY
        elif self.ai_provider == "zhipu":
            self.zhipu_client = ZhipuAI(api_key=settings.ZHIPU_API_KEY)
        
    async def analyze_emotion(self, text: str) -> Dict:
        """
        分析文本情感
        
        Args:
            text: 用户输入的文本
            
        Returns:
            {
                "valence": 0.75,  # 效价 (0-1)
                "arousal": 0.5,   # 唤起度 (0-1)
                "primary_emotion": "joy",
                "emotion_scores": {"joy": 0.8, "calm": 0.6, ...}
            }
        """
        try:
            # 构建 prompt
            prompt = f"""
分析以下文本的情感，返回JSON格式：

文本："{text}"

请分析并返回：
1. valence（效价）：0-1之间的小数，0=消极，1=积极
2. arousal（唤起度）：0-1之间的小数，0=平静，1=激动
3. primary_emotion（主要情绪）：选择一个最主要的情绪词（英文）
4. emotion_scores（各情绪得分）：对以下情绪分别打分（0-1）：
   - joy（快乐）
   - calm（平静）
   - sadness（悲伤）
   - anxiety（焦虑）
   - anger（愤怒）
   - excitement（兴奋）

只返回JSON，不要其他解释。格式：
{{"valence": 0.0, "arousal": 0.0, "primary_emotion": "xxx", "emotion_scores": {{"joy": 0.0, ...}}}}
"""
            
            # 根据配置调用不同的 AI API
            if self.ai_provider == "openai":
                response = await openai.chat.completions.create(
                    model=settings.OPENAI_MODEL_EMOTION,
                    messages=[
                        {"role": "system", "content": "你是一个专业的情感分析助手。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                content = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "zhipu":
                response = self.zhipu_client.chat.completions.create(
                    model=settings.ZHIPU_MODEL_EMOTION,
                    messages=[
                        {"role": "system", "content": "你是一个专业的情感分析助手。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=300
                )
                content = response.choices[0].message.content.strip()
            else:
                raise ValueError(f"不支持的 AI 提供商: {self.ai_provider}")
            
            # 解析返回结果
            emotion_data = json.loads(content)
            
            return emotion_data
            
        except Exception as e:
            print(f"Emotion analysis error: {e}")
            # 降级：返回中性情感
            return {
                "valence": 0.5,
                "arousal": 0.5,
                "primary_emotion": "neutral",
                "emotion_scores": {
                    "joy": 0.3,
                    "calm": 0.5,
                    "sadness": 0.2,
                    "anxiety": 0.2,
                    "anger": 0.1,
                    "excitement": 0.2
                }
            }
    
    def emotion_to_color(self, valence: float, arousal: float) -> str:
        """
        将情感映射到颜色
        
        基于情绪二维模型：
        - 高效价+高唤起 (兴奋、快乐) → 明亮黄色、橙色
        - 高效价+低唤起 (平静、满足) → 薄荷绿、淡蓝色
        - 低效价+高唤起 (焦虑、愤怒) → 深红色、暗紫色
        - 低效价+低唤起 (悲伤、低落) → 灰蓝色、暗灰色
        
        Args:
            valence: 效价 (0-1)
            arousal: 唤起度 (0-1)
            
        Returns:
            HEX颜色值，如 "#87CEEB"
        """
        # 限制范围
        valence = max(0.0, min(1.0, valence))
        arousal = max(0.0, min(1.0, arousal))
        
        # 色相 (Hue): 基于效价
        # 高效价 → 暖色系 (黄、橙)，低效价 → 冷色系 (蓝、紫)
        if valence >= 0.5:
            # 积极情绪：黄色(60°)到绿色(120°)
            hue = 60 + (valence - 0.5) * 2 * 60  # 60° - 120°
        else:
            # 消极情绪：蓝色(240°)到紫色(300°)
            hue = 240 + valence * 2 * 60  # 180° - 240°
        
        # 饱和度 (Saturation): 基于唤起度
        # 高唤起 → 高饱和度，低唤起 → 低饱和度
        saturation = 0.3 + arousal * 0.6  # 0.3 - 0.9
        
        # 亮度 (Value/Lightness): 基于效价和唤起度的组合
        # 高效价 → 较亮，低效价 → 较暗
        lightness = 0.4 + valence * 0.4  # 0.4 - 0.8
        
        # HSL 转 RGB
        r, g, b = colorsys.hls_to_rgb(hue / 360, lightness, saturation)
        
        # 转换为 HEX
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
        
        return hex_color
    
    def calculate_daily_emotion(self, emotions: list) -> Tuple[float, float]:
        """
        计算当日综合情感（多条记录的加权平均）
        
        Args:
            emotions: 情感数据列表，按时间顺序
                     [{"valence": 0.8, "arousal": 0.6}, ...]
        
        Returns:
            (综合valence, 综合arousal)
        """
        if not emotions:
            return 0.5, 0.5
        
        n = len(emotions)
        total_weight = 0
        weighted_valence = 0
        weighted_arousal = 0
        
        # 指数衰减权重：最近的记录权重最高
        for i, emotion in enumerate(emotions):
            weight = math.pow(0.8, n - i - 1)  # 0.8^(n-i-1)
            total_weight += weight
            weighted_valence += emotion["valence"] * weight
            weighted_arousal += emotion["arousal"] * weight
        
        # 归一化
        final_valence = weighted_valence / total_weight
        final_arousal = weighted_arousal / total_weight
        
        return final_valence, final_arousal


# 单例
emotion_service = EmotionService()
