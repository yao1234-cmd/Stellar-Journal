'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Calendar, ChevronLeft, ChevronRight } from 'lucide-react'
import { planetApi, PlanetHistoryItem } from '@/lib/api'
import { usePlanetStore } from '@/stores/planetStore'

export default function TimelinePanel() {
  const [history, setHistory] = useState<PlanetHistoryItem[]>([])
  const [expanded, setExpanded] = useState(false)
  const [days, setDays] = useState(7)
  const { fetchPlanetState } = usePlanetStore()

  useEffect(() => {
    loadHistory()
  }, [days])

  const loadHistory = async () => {
    try {
      const data = await planetApi.getHistory(days)
      setHistory(data.history)
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const handleDateClick = async (date: string) => {
    await fetchPlanetState(date)
  }

  return (
    <motion.div
      initial={{ x: 100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="glass-effect rounded-2xl overflow-hidden"
    >
      {/* 头部 */}
      <div
        className="p-4 flex items-center gap-2 cursor-pointer hover:bg-white/5 transition-colors"
        onClick={() => setExpanded(!expanded)}
      >
        <Calendar className="w-5 h-5 text-white" />
        <span className="text-white font-medium">时光轴</span>
        <motion.div
          animate={{ rotate: expanded ? 90 : -90 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronLeft className="w-4 h-4 text-white/70" />
        </motion.div>
      </div>

      {/* 时间线 */}
      {expanded && (
        <motion.div
          initial={{ height: 0 }}
          animate={{ height: 'auto' }}
          exit={{ height: 0 }}
          className="border-t border-white/10"
        >
          {/* 天数选择 */}
          <div className="p-4 flex gap-2">
            {[7, 14, 30].map((d) => (
              <button
                key={d}
                onClick={() => setDays(d)}
                className={`px-3 py-1 rounded text-sm transition-all ${
                  days === d
                    ? 'bg-white/20 text-white'
                    : 'bg-white/5 text-white/60 hover:bg-white/10'
                }`}
              >
                {d}天
              </button>
            ))}
          </div>

          {/* 历史列表 */}
          <div className="max-h-96 overflow-y-auto p-4 space-y-2">
            {history.slice().reverse().map((item, index) => (
              <motion.button
                key={item.date}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.02 }}
                onClick={() => handleDateClick(item.date)}
                className="w-full flex items-center gap-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 transition-all group"
              >
                {/* 颜色指示器 */}
                <div
                  className="w-8 h-8 rounded-full flex-shrink-0 border-2 border-white/20 group-hover:scale-110 transition-transform"
                  style={{ backgroundColor: item.atmosphere_color }}
                />

                {/* 日期和记录数 */}
                <div className="flex-1 text-left">
                  <div className="text-sm text-white font-medium">
                    {formatDate(item.date)}
                  </div>
                  <div className="text-xs text-white/60">
                    {item.record_count} 条记录
                  </div>
                </div>

                <ChevronRight className="w-4 h-4 text-white/40 group-hover:text-white/80 transition-colors" />
              </motion.button>
            ))}

            {history.length === 0 && (
              <div className="text-center text-white/40 py-8">
                暂无历史记录
              </div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return '今天'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return '昨天'
  } else {
    return date.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
  }
}
