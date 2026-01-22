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
    try {      const state = await planetApi.getState(date) as any      set({ planetState: state, loading: false })
    } catch (error: any) {      set({ error: error.message, loading: false })
    }
  },

  // 获取统计信息
  fetchStats: async () => {
    try {      const stats = await planetApi.getStats() as any      set({ stats })
    } catch (error: any) {      console.error('Failed to fetch stats:', error)
    }
  },

  // 刷新星球
  refreshPlanet: async () => {
    await get().fetchPlanetState()
    await get().fetchStats()
  },
}))
