'use client'

import { useMemo } from 'react'
import { motion } from 'framer-motion'
import { Sparkles } from 'lucide-react'

interface SplashScreenProps {
  show: boolean
  onComplete: () => void
}

export default function SplashScreen({ show, onComplete }: SplashScreenProps) {
  // 预计算星星位置和动画延迟，避免水合不匹配
  const stars = useMemo(() => 
    Array.from({ length: 50 }).map((_, i) => ({
      left: Math.random() * 100,
      top: Math.random() * 100,
      delay: Math.random() * 2,
      scale: 0.5 + Math.random() * 0.5,
    })),
    []
  )
  return (
    <motion.div
      initial={{ opacity: 1 }}
      animate={{ opacity: show ? 1 : 0 }}
      transition={{ duration: 0.5 }}
      onAnimationComplete={() => {
        if (!show) {
          onComplete()
        }
      }}
      className="fixed inset-0 z-[100] flex items-center justify-center bg-gradient-to-b from-indigo-950 via-purple-900 to-slate-900"
      style={{
        pointerEvents: show ? 'auto' : 'none',
      }}
    >
          {/* 星空背景动画 */}
          <div className="absolute inset-0 overflow-hidden">
            {stars.map((star, i) => (
              <motion.div
                key={i}
                className="absolute w-1 h-1 bg-white rounded-full"
                style={{
                  left: `${star.left}%`,
                  top: `${star.top}%`,
                }}
                initial={{ opacity: 0, scale: 0 }}
                animate={{
                  opacity: [0, 1, 0],
                  scale: [0, star.scale, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: star.delay,
                }}
              />
            ))}
          </div>

          {/* 主要内容 */}
          <div className="relative z-10 text-center px-8 max-w-3xl">
            {/* Logo 图标 */}
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ 
                type: 'spring', 
                stiffness: 200, 
                damping: 20,
                delay: 0.2 
              }}
              className="mb-8 flex justify-center"
            >
              <div className="relative">
                <Sparkles className="w-16 h-16 text-yellow-300" />
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  className="absolute inset-0"
                >
                  <Sparkles className="w-16 h-16 text-yellow-300/30" />
                </motion.div>
              </div>
            </motion.div>

            {/* 标题 */}
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.8 }}
              className="text-5xl font-bold text-white mb-4"
            >
              星迹 Stellar Journal
            </motion.h1>

            {/* 分隔线 */}
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="h-px bg-gradient-to-r from-transparent via-white/50 to-transparent mb-8"
            />

            {/* 座右铭 */}
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.2, duration: 0.8 }}
              className="text-2xl text-white/90 leading-relaxed"
            >
              让每一次内心波动
            </motion.p>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.5, duration: 0.8 }}
              className="text-2xl text-white/90 leading-relaxed"
            >
              都成为构建独特宇宙的星辰
            </motion.p>

            {/* 光晕效果 */}
            <motion.div
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 2, opacity: [0, 0.3, 0] }}
              transition={{ delay: 1, duration: 2, repeat: Infinity }}
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-purple-500/20 rounded-full blur-3xl -z-10"
            />
          </div>
        </motion.div>
  )
}
