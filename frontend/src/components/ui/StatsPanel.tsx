'use client'

import { useEffect } from 'react'
import { motion } from 'framer-motion'
import { Heart, Sparkles, MessageSquare, Calendar } from 'lucide-react'
import { usePlanetStore } from '@/stores/planetStore'

export default function StatsPanel() {
  const { stats, fetchStats } = usePlanetStore()

  useEffect(() => {
    fetchStats()
  }, [fetchStats])

  if (!stats) return null

  const statItems = [
    { icon: Heart, label: '心情', value: stats.mood_count, color: 'text-pink-400' },
    { icon: Sparkles, label: '灵感', value: stats.spark_count, color: 'text-yellow-400' },
    { icon: MessageSquare, label: '思考', value: stats.thought_count, color: 'text-green-400' },
    { icon: Calendar, label: '活跃', value: `${stats.days_active}天`, color: 'text-blue-400' },
  ]

  return (
    <motion.div
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass-effect rounded-2xl px-6 py-3 flex items-center gap-6"
    >
      {statItems.map(({ icon: Icon, label, value, color }, index) => (
        <motion.div
          key={label}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="flex items-center gap-2"
        >
          <Icon className={`w-4 h-4 ${color}`} />
          <div className="text-sm">
            <span className="text-white/60">{label}</span>
            <span className="text-white font-semibold ml-1">{value}</span>
          </div>
        </motion.div>
      ))}
    </motion.div>
  )
}
