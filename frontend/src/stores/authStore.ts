/**
 * Authentication Store
 * 管理用户认证状态、Token 存储和刷新
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
  
  // Actions
  setAuth: (accessToken: string, refreshToken: string, user: User) => void
  clearAuth: () => void
  setUser: (user: User) => void
  setLoading: (loading: boolean) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      
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
    }),
    {
      name: 'auth-storage', // localStorage key
      partialize: (state) => ({ 
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
