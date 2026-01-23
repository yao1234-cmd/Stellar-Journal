/**
 * Authentication Store
 * 管理用户认证状态、Token 存储和刷新
 * 
 * Token 持久化策略：
 * - Access Token 有效期：7 天
 * - Refresh Token 有效期：30 天
 * - Token 存储在 localStorage 以支持 7 天自动登录
 */
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  username: string
  email: string
  is_email_verified: boolean
  created_at: string
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  _hasHydrated: boolean
  
  // Actions
  setAuth: (accessToken: string, refreshToken: string, user: User) => void
  clearAuth: () => void
  setUser: (user: User) => void
  setLoading: (loading: boolean) => void
  setHasHydrated: (hasHydrated: boolean) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      _hasHydrated: false,
      
      setAuth: (accessToken, refreshToken, user) => set({
        accessToken,
        refreshToken,
        user,
        isAuthenticated: true,
      }),
      
      clearAuth: () => set({
        user: null,
        accessToken: null,
        refreshToken: null,
        isAuthenticated: false,
      }),
      
      setUser: (user) => set({ user }),
      
      setLoading: (loading) => set({ isLoading: loading }),
      
      setHasHydrated: (hasHydrated) => set({ _hasHydrated: hasHydrated }),
    }),
    {
      name: 'auth-storage', // localStorage key
      // 持久化 token 以支持 7 天自动登录
      partialize: (state) => ({ 
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
      onRehydrateStorage: () => (state) => {
        // Hydration 完成后设置标志
        state?.setHasHydrated(true)
      },
    }
  )
)
