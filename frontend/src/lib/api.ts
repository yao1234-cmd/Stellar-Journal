/**
 * API Client - 后端接口调用
 */
import axios from 'axios'

// 临时硬编码 API URL 用于调试
const API_BASE_URL = 'http://localhost:8000/api/v1'
console.log('🔗 API Base URL:', API_BASE_URL)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加 token
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// ========== 记录相关 API ==========

export interface RecordCreate {
  type: 'mood' | 'spark' | 'thought'
  content: string
  audio_url?: string
}

export interface EmotionData {
  valence: number
  arousal: number
  primary_emotion: string
  emotion_scores: Record<string, number>
}

export interface Record {
  id: string
  user_id: string
  type: 'mood' | 'spark' | 'thought'
  content: string
  audio_url?: string
  emotion_analysis?: EmotionData
  keywords?: string[]
  theme_cluster?: string
  color_hex?: string
  position_data?: {
    x?: number
    y?: number
    z?: number
    orbit_radius?: number
    orbit_angle?: number
  }
  created_at: string
  updated_at?: string
}

export const recordsApi = {
  // 创建记录
  create: (data: RecordCreate) => api.post<Record>('/records/', data),

  // 获取记录列表
  list: (params?: { skip?: number; limit?: number; record_type?: string }) =>
    api.get<{ records: Record[]; total: number; page: number; page_size: number }>(
      '/records/',
      { params }
    ),

  // 获取单条记录
  get: (id: string) => api.get<Record>(`/records/${id}`),

  // 删除记录
  delete: (id: string) => api.delete(`/records/${id}`),

  // 语音转文字
  transcribe: (audioFile: File) => {
    const formData = new FormData()
    formData.append('audio', audioFile)
    return api.post<{ text: string; success: boolean }>('/records/transcribe', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// ========== 星球相关 API ==========

export interface StarElement {
  id: string
  position: Record<string, number>
  color: string
  size: number
  keyword: string
}

export interface TreeElement {
  id: string
  position: Record<string, number>
  theme: string
  leaf_count: number
  size: number
}

export interface PlanetState {
  date: string
  atmosphere_color: string
  stars: StarElement[]
  trees: TreeElement[]
  total_records: number
}

export interface PlanetHistoryItem {
  date: string
  atmosphere_color: string
  record_count: number
}

export interface PlanetHistory {
  history: PlanetHistoryItem[]
  start_date: string
  end_date: string
}

export interface PlanetStats {
  total_records: number
  mood_count: number
  spark_count: number
  thought_count: number
  start_date?: string
  days_active: number
}

export const planetApi = {
  // 获取星球状态
  getState: (date?: string) => {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.ts:151',message:'Calling getState API',data:{date,url:`${API_BASE_URL}/planet/state`},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
    // #endregion
    return api.get<PlanetState>('/planet/state', { params: { target_date: date } })
  },

  // 获取历史数据
  getHistory: (days: number = 30) => {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.ts:159',message:'Calling getHistory API',data:{days,url:`${API_BASE_URL}/planet/history`},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
    // #endregion
    return api.get<PlanetHistory>('/planet/history', { params: { days } })
  },

  // 获取统计信息
  getStats: () => {
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.ts:167',message:'Calling getStats API',data:{url:`${API_BASE_URL}/planet/stats`},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
    // #endregion
    return api.get<PlanetStats>('/planet/stats')
  },
}

export default api
