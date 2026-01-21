"""
Whisper Service - 语音转文字服务
"""
import openai
from app.core.config import settings
from typing import BinaryIO


class WhisperService:
    """语音转文字服务"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def transcribe(self, audio_file: BinaryIO, language: str = "zh") -> str:
        """
        将音频转换为文字
        
        Args:
            audio_file: 音频文件对象
            language: 语言代码，默认中文
            
        Returns:
            转写的文本
        """
        try:
            response = await openai.audio.transcriptions.create(
                model=settings.OPENAI_MODEL_WHISPER,
                file=audio_file,
                language=language,
                response_format="text"
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            raise


# 单例
whisper_service = WhisperService()
