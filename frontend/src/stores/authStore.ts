/**
 * Authentication Store
 * 管理用户认证状态、Token 存储和刷新
 * 
 * 安全注意：Token 不再持久化到 localStorage 以防止 XSS 攻击
 * Token 仅保存在内存中，页面刷新后需要重新登录
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
      // 安全优化：不再持久化敏感 token，仅持久化用户信息和登录状态标志
      partialize: (state) => ({ 
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        // accessToken 和 refreshToken 不再持久化
        // 这意味着刷新页面后需要重新登录，但更安全
      }),
      onRehydrateStorage: () => (state) => {
        // Hydration 完成后设置标志
        state?.setHasHydrated(true)
      },
    }
  )
)
