/**
 * Planet Store - 星球状态管理
 */
import { create } from 'zustand'
import { PlanetState, PlanetStats, planetApi } from '@/lib/api'

interface PlanetStore {
  // 状态
  planetState: PlanetState | null
  stats: PlanetStats | null
  loading: boolean
  error: string | null

  // 动作
  fetchPlanetState: (date?: string) => Promise<void>
  fetchStats: () => Promise<void>
  refreshPlanet: () => Promise<void>
}

export const usePlanetStore = create<PlanetStore>((set, get) => ({
  // 初始状态
  planetState: null,
  stats: null,
  loading: false,
  error: null,

  // 获取星球状态
  fetchPlanetState: async (date?: string) => {
    set({ loading: true, error: null })
    try {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'planetStore.ts:31',message:'Fetching planet state',data:{date},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      const { data: state } = await planetApi.getState(date)
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'planetStore.ts:35',message:'Planet state fetched successfully',data:{state},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      set({ planetState: state, loading: false })
    } catch (error: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'planetStore.ts:40',message:'Failed to fetch planet state',data:{error:error.message,stack:error.stack},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      set({ error: error.message, loading: false })
    }
  },

  // 获取统计信息
  fetchStats: async () => {
    try {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'planetStore.ts:50',message:'Fetching stats',data:{},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      const { data: stats } = await planetApi.getStats()
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'planetStore.ts:54',message:'Stats fetched successfully',data:{stats},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      set({ stats })
    } catch (error: any) {
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/0177d4de-2faa-4d99-960c-3205811fe5c0',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'planetStore.ts:59',message:'Failed to fetch stats',data:{error:error.message,stack:error.stack},timestamp:Date.now(),sessionId:'debug-session',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      console.error('Failed to fetch stats:', error)
    }
  },

  // 刷新星球
  refreshPlanet: async () => {
    await get().fetchPlanetState()
    await get().fetchStats()
  },
}))
