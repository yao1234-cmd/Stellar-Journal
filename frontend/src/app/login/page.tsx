'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Mail, Lock, LogIn, Sparkles } from 'lucide-react'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/stores/authStore'

export default function LoginPage() {
  const router = useRouter()
  const setAuth = useAuthStore((state) => state.setAuth)
  
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const tokenResponse = await authApi.login({ email, password }) as any
      
      // 先保存token到store（这样axios拦截器才能在下一个请求中使用）
      setAuth(tokenResponse.access_token, tokenResponse.refresh_token, null as any)
      
      // 然后获取用户信息（此时token已经在localStorage中，拦截器会自动添加）
      const userResponse = await authApi.getCurrentUser() as any

      // 更新完整的认证信息
      setAuth(tokenResponse.access_token, tokenResponse.refresh_token, userResponse)

      // 跳转到主页
      router.push('/')
    } catch (err: any) {
      let errorMsg = '登录失败，请检查邮箱和密码'
      
      if (err.response?.data?.detail) {
        const detail = err.response.data.detail
        // Handle Pydantic validation errors (array of objects)
        if (Array.isArray(detail) && detail.length > 0) {
          errorMsg = detail[0].msg || detail[0].message || errorMsg
        } 
        // Handle string error
        else if (typeof detail === 'string') {
          errorMsg = detail
        }
        // Handle object error
        else if (typeof detail === 'object' && detail.msg) {
          errorMsg = detail.msg
        }
      }
      
      setError(errorMsg)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4 overflow-hidden relative">
      {/* 星空背景 */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(100)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-white rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              opacity: Math.random() * 0.7 + 0.3,
            }}
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: Math.random() * 3 + 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>

      {/* 登录卡片 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 w-full max-w-md relative z-10 shadow-2xl border border-white/20"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
            className="inline-block"
          >
            <Sparkles className="w-12 h-12 text-yellow-300 mx-auto" />
          </motion.div>
          <h1 className="text-3xl font-bold text-white mt-4">Stellar Journal</h1>
          <p className="text-white/70 mt-2">记录你的情感星球</p>
        </div>

        {/* 错误提示 */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-lg mb-6"
          >
            {error}
          </motion.div>
        )}

        {/* 登录表单 */}
        <form onSubmit={handleLogin} className="space-y-6">
          {/* 邮箱 */}
          <div>
            <label className="block text-white/90 mb-2 text-sm font-medium">
              邮箱
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full bg-white/10 border border-white/20 rounded-lg pl-11 pr-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="your@email.com"
              />
            </div>
          </div>

          {/* 密码 */}
          <div>
            <label className="block text-white/90 mb-2 text-sm font-medium">
              密码
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
                className="w-full bg-white/10 border border-white/20 rounded-lg pl-11 pr-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="••••••••"
              />
            </div>
          </div>

          {/* 登录按钮 */}
          <motion.button
            type="submit"
            disabled={isLoading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-2 hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <LogIn className="w-5 h-5" />
                登录
              </>
            )}
          </motion.button>
        </form>

        {/* 注册链接 */}
        <div className="mt-6 text-center">
          <p className="text-white/70">
            还没有账号？{' '}
            <Link href="/register" className="text-purple-300 hover:text-purple-200 font-medium">
              立即注册
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}
