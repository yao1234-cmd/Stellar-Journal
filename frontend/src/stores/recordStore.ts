/**
 * Record Store - 记录状态管理
 */
import { create } from 'zustand'
import { RecordItem, RecordCreate, recordsApi } from '@/lib/api'

interface RecordStore {
  // 状态
  records: RecordItem[]
  currentRecord: RecordItem | null
  loading: boolean
  error: string | null

  // 动作
  fetchRecords: (params?: { skip?: number; limit?: number; record_type?: string }) => Promise<void>
  createRecord: (data: RecordCreate) => Promise<RecordItem | null>
  deleteRecord: (id: string) => Promise<void>
  transcribeAudio: (file: File) => Promise<string | null>
}

export const useRecordStore = create<RecordStore>((set) => ({
  // 初始状态
  records: [],
  currentRecord: null,
  loading: false,
  error: null,

  // 获取记录列表
  fetchRecords: async (params) => {
    set({ loading: true, error: null })
    try {
      const response = await recordsApi.list(params) as any
      set({ records: response.records || [], loading: false })
    } catch (error: any) {
      set({ error: error.message, loading: false })
    }
  },

  // 创建记录
  createRecord: async (data) => {
    set({ loading: true, error: null })
    try {
      const record = await recordsApi.create(data) as any
      set((state) => ({
        records: [record, ...state.records],
        currentRecord: record,
        loading: false,
      }))
      return record
    } catch (error: any) {
      console.error('❌ 创建记录失败:', error)
      set({ error: error.message, loading: false })
      return null
    }
  },

  // 删除记录
  deleteRecord: async (id) => {
    set({ loading: true, error: null })
    try {
      await recordsApi.delete(id)
      set((state) => ({
        records: state.records.filter((r) => r.id !== id),
        loading: false,
      }))
    } catch (error: any) {
      set({ error: error.message, loading: false })
    }
  },

  // 语音转文字
  transcribeAudio: async (file) => {
    set({ loading: true, error: null })
    try {
      const { data: result } = await recordsApi.transcribe(file)
      set({ loading: false })
      return result.text
    } catch (error: any) {
      set({ error: error.message, loading: false })
      return null
    }
  },
}))
