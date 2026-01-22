'use client'

import { useEffect, useState, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { CheckCircle, XCircle, Loader2, Sparkles } from 'lucide-react'
import { authApi } from '@/lib/api'

function VerifyEmailContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get('token')
  
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (!token) {
      setStatus('error')
      setMessage('验证链接无效')
      return
    }

    const verifyEmail = async () => {
      try {
        const response = await authApi.verifyEmail(token) as any
        setStatus('success')
        setMessage(response.message || '邮箱验证成功！')
        
        // 3秒后跳转登录页
        setTimeout(() => {
          router.push('/login')
        }, 3000)
      } catch (err: any) {
        setStatus('error')
        setMessage(err.response?.data?.detail || '验证失败，请重试')
      }
    }

    verifyEmail()
  }, [token, router])

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

      {/* 验证状态卡片 */}
      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 w-full max-w-md relative z-10 shadow-2xl border border-white/20 text-center"
      >
        {status === 'loading' && (
          <>
            <Loader2 className="w-20 h-20 text-purple-400 mx-auto mb-6 animate-spin" />
            <h2 className="text-2xl font-bold text-white mb-4">正在验证...</h2>
            <p className="text-white/80">请稍候，我们正在验证您的邮箱</p>
          </>
        )}

        {status === 'success' && (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring" }}
            >
              <CheckCircle className="w-20 h-20 text-green-400 mx-auto mb-6" />
            </motion.div>
            
            <h2 className="text-2xl font-bold text-white mb-4">验证成功！</h2>
            <p className="text-white/80 mb-6">{message}</p>
            <p className="text-white/60 text-sm">3 秒后自动跳转到登录页...</p>
            
            <Link href="/login">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="mt-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold px-8 py-3 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all"
              >
                立即登录
              </motion.button>
            </Link>
          </>
        )}

        {status === 'error' && (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring" }}
            >
              <XCircle className="w-20 h-20 text-red-400 mx-auto mb-6" />
            </motion.div>
            
            <h2 className="text-2xl font-bold text-white mb-4">验证失败</h2>
            <p className="text-white/80 mb-6">{message}</p>
            
            <Link href="/register">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold px-8 py-3 rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all"
              >
                重新注册
              </motion.button>
            </Link>
          </>
        )}
      </motion.div>
    </div>
  )
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-b from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-white animate-spin" />
      </div>
    }>
      <VerifyEmailContent />
    </Suspense>
  )
}
