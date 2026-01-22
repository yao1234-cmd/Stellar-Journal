/**
 * API Client - 后端接口调用
 */
import axios from 'axios'

// API URL - 从环境变量读取，本地开发时使用 localhost
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
console.log('🔗 API Base URL:', API_BASE_URL)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// 请求拦截器 - 自动注入 token
api.interceptors.request.use(
  (config) => {
    // 从 localStorage 读取 token（因为 zustand persist）
    const authStorage = localStorage.getItem('auth-storage')
    if (authStorage) {
      try {
        const { state } = JSON.parse(authStorage)
        if (state?.accessToken) {
          config.headers.Authorization = `Bearer ${state.accessToken}`
        }
      } catch (e) {
        console.error('Failed to parse auth storage:', e)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理 401 和自动刷新 token
api.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const originalRequest = error.config
    
    // 如果是 401 且未尝试刷新过
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        // 尝试刷新 token
        const authStorage = localStorage.getItem('auth-storage')
        if (authStorage) {
          const { state } = JSON.parse(authStorage)
          if (state?.refreshToken) {
            const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: state.refreshToken
            })
            
            // 更新 token
            const { access_token, refresh_token } = response.data
            const newState = {
              ...state,
              accessToken: access_token,
              refreshToken: refresh_token,
            }
            localStorage.setItem('auth-storage', JSON.stringify({ state: newState }))
            
            // 重试原请求
            originalRequest.headers.Authorization = `Bearer ${access_token}`
            return api(originalRequest)
          }
        }
      } catch (refreshError) {
        // 刷新失败，清除认证状态并跳转登录
        localStorage.removeItem('auth-storage')
        if (typeof window !== 'undefined') {
          window.location.href = '/login'
        }
        return Promise.reject(refreshError)
      }
    }
    
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

export interface RecordItem {
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
  create: (data: RecordCreate) => api.post<RecordItem>('/records/', data),

  // 获取记录列表
  list: (params?: { skip?: number; limit?: number; record_type?: string }) =>
    api.get<{ records: RecordItem[]; total: number; page: number; page_size: number }>(
      '/records/',
      { params }
    ),

  // 获取单条记录
  get: (id: string) => api.get<RecordItem>(`/records/${id}`),

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

// ========== 认证相关 API ==========

export interface UserRegister {
  username: string
  email: string
  password: string
}

export interface UserLogin {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserResponse {
  id: string
  username: string
  email: string
  is_active: boolean
  is_email_verified: boolean
  created_at: string
}

export interface MessageResponse {
  message: string
}

export const authApi = {
  // 注册
  register: (data: UserRegister) => {
    return api.post<MessageResponse>('/auth/register', data)
  },

  // 验证邮箱
  verifyEmail: (token: string) => {
    return api.post<MessageResponse>('/auth/verify-email', { token })
  },

  // 登录
  login: (data: UserLogin) => {
    return api.post<TokenResponse>('/auth/login', data)
  },

  // 刷新 token
  refreshToken: (refreshToken: string) => {
    return api.post<TokenResponse>('/auth/refresh', { refresh_token: refreshToken })
  },

  // 获取当前用户信息
  getCurrentUser: () => {
    return api.get<UserResponse>('/auth/me')
  },

  // 重新发送验证邮件
  resendVerification: (email: string) => {
    return api.post<MessageResponse>('/auth/resend-verification', { email })
  },
}

export default api
