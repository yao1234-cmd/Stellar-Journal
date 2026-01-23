'use client'

import { useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { Mail, Lock, User, Sparkles, CheckCircle } from 'lucide-react'
import { authApi } from '@/lib/api'

// 简单的伪随机数生成器（seeded PRNG）用于确定性星星生成
function mulberry32(seed: number) {
  return function() {
    let t = seed += 0x6D2B79F5
    t = Math.imul(t ^ t >>> 15, t | 1)
    t ^= t + Math.imul(t ^ t >>> 7, t | 61)
    return ((t ^ t >>> 14) >>> 0) / 4294967296
  }
}

// 预计算星星数据
function generateStars(count: number, seed: number = 12345) {
  const rng = mulberry32(seed)
  return Array.from({ length: count }, () => ({
    left: rng() * 100,
    top: rng() * 100,
    opacity: rng() * 0.7 + 0.3,
    duration: rng() * 3 + 2,
    delay: rng() * 2,
  }))
}

export default function RegisterPage() {
  const router = useRouter()
  
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  
  // 使用 useMemo 预计算星星，避免 SSR/客户端不匹配
  const stars = useMemo(() => generateStars(100), [])

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    // 验证密码
    if (password !== confirmPassword) {
      setError('两次输入的密码不一致')
      return
    }
    
    if (password.length < 8) {
      setError('密码长度至少为 8 个字符')
      return
    }
    
    if (!/\d/.test(password)) {
      setError('密码必须包含至少一个数字')
      return
    }
    
    if (!/[a-zA-Z]/.test(password)) {
      setError('密码必须包含至少一个字母')
      return
    }

    setIsLoading(true)

    try {
      await authApi.register({ username, email, password }) as any
      setSuccess(true)
    } catch (err: any) {
      let errorMsg = '注册失败，请稍后重试'
      
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

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4 overflow-hidden relative">
        {/* 星空背景 */}
        <div className="absolute inset-0 overflow-hidden">
          {stars.map((star, i) => (
            <motion.div
              key={i}
              className="absolute w-1 h-1 bg-white rounded-full"
              style={{
                left: `${star.left}%`,
                top: `${star.top}%`,
                opacity: star.opacity,
              }}
              animate={{
                scale: [1, 1.5, 1],
                opacity: [0.3, 0.8, 0.3],
              }}
              transition={{
                duration: star.duration,
                repeat: Infinity,
                delay: star.delay,
              }}
            />
          ))}
        </div>

        {/* 成功提示 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 w-full max-w-md relative z-10 shadow-2xl border border-white/20 text-center"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring" }}
          >
            <CheckCircle className="w-20 h-20 text-green-400 mx-auto mb-6" />
          </motion.div>
          
          <h2 className="text-2xl font-bold text-white mb-4">注册成功！</h2>
          <p className="text-white/80 mb-6">
            我们已向您的邮箱发送了一封验证邮件，请查收并点击链接验证您的邮箱。
          </p>
          
          <Link href="/login">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold px-8 py-3 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all"
            >
              前往登录
            </motion.button>
          </Link>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4 overflow-hidden relative">
      {/* 星空背景 */}
      <div className="absolute inset-0 overflow-hidden">
        {stars.map((star, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-white rounded-full"
            style={{
              left: `${star.left}%`,
              top: `${star.top}%`,
              opacity: star.opacity,
            }}
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: star.duration,
              repeat: Infinity,
              delay: star.delay,
            }}
          />
        ))}
      </div>

      {/* 注册卡片 */}
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
          <h1 className="text-3xl font-bold text-white mt-4">加入 Stellar Journal</h1>
          <p className="text-white/70 mt-2">开始记录你的情感星球</p>
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

        {/* 注册表单 */}
        <form onSubmit={handleRegister} className="space-y-5">
          {/* 用户名 */}
          <div>
            <label className="block text-white/90 mb-2 text-sm font-medium">
              用户名
            </label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                minLength={3}
                maxLength={50}
                className="w-full bg-white/10 border border-white/20 rounded-lg pl-11 pr-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="你的用户名"
              />
            </div>
          </div>

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
                placeholder="至少 8 位，包含字母和数字"
              />
            </div>
          </div>

          {/* 确认密码 */}
          <div>
            <label className="block text-white/90 mb-2 text-sm font-medium">
              确认密码
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                minLength={8}
                className="w-full bg-white/10 border border-white/20 rounded-lg pl-11 pr-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400"
                placeholder="再次输入密码"
              />
            </div>
          </div>

          {/* 注册按钮 */}
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
                <Sparkles className="w-5 h-5" />
                注册
              </>
            )}
          </motion.button>
        </form>

        {/* 登录链接 */}
        <div className="mt-6 text-center">
          <p className="text-white/70">
            已有账号？{' '}
            <Link href="/login" className="text-purple-300 hover:text-purple-200 font-medium">
              立即登录
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}
