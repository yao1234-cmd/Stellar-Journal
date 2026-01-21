'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Calendar, Heart, Sparkles, MessageCircle, ChevronDown } from 'lucide-react'
import { useRecordStore } from '@/stores/recordStore'

type RecordType = 'mood' | 'spark' | 'thought'

interface EmotionAnalysis {
  valence: number
  arousal: number
  primary_emotion: string
  emotion_scores: Record<string, number>
}

interface JournalRecord {
  id: string
  type: RecordType
  content: string
  emotion?: EmotionAnalysis  // 情感分析对象
  keywords?: string[]        // 关键词数组
  theme?: string
  created_at: string
}

const typeConfig = {
  mood: { icon: Heart, label: '心情', color: 'text-pink-400', bg: 'bg-pink-500/10' },
  spark: { icon: Sparkles, label: '灵感', color: 'text-yellow-400', bg: 'bg-yellow-500/10' },
  thought: { icon: MessageCircle, label: '思考', color: 'text-green-400', bg: 'bg-green-500/10' },
}

export default function RecordDrawer() {
  const [isOpen, setIsOpen] = useState(false)
  const [records, setRecords] = useState<JournalRecord[]>([])
  const [selectedType, setSelectedType] = useState<RecordType | 'all'>('all')
  const [expandedId, setExpandedId] = useState<string | null>(null)

  // 加载记录
  useEffect(() => {
    if (isOpen) {
      fetchRecords()
    }
  }, [isOpen])

  const fetchRecords = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/records/history?days=30')
      const data = await response.json()
      
      // 确保返回的是数组
      if (Array.isArray(data)) {
        setRecords(data)
      } else {
        console.warn('API 返回的不是数组:', data)
        setRecords([])
      }
    } catch (error) {
      console.error('加载记录失败:', error)
      setRecords([])
    }
  }

  // 确保 records 是数组
  const safeRecords = Array.isArray(records) ? records : []
  
  const filteredRecords = selectedType === 'all' 
    ? safeRecords 
    : safeRecords.filter(r => r.type === selectedType)

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    const now = new Date()
    const diffTime = now.getTime() - date.getTime()
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return '今天'
    if (diffDays === 1) return '昨天'
    if (diffDays < 7) return `${diffDays}天前`
    
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  }

  return (
    <>
      {/* 触发按钮 */}
      <motion.button
        onClick={() => setIsOpen(true)}
        className="fixed top-6 right-6 z-40 px-4 py-2 bg-white/10 hover:bg-white/20 backdrop-blur-md rounded-full text-white transition-all shadow-lg"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Calendar className="w-5 h-5 inline mr-2" />
        时光轴
      </motion.button>

      {/* 抽屉面板 */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* 背景遮罩 */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            />

            {/* 抽屉内容 */}
            <motion.div
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="fixed top-0 right-0 h-full w-full max-w-md bg-gradient-to-br from-slate-900 to-slate-800 shadow-2xl z-50 overflow-hidden"
            >
              {/* 头部 */}
              <div className="p-6 bg-white/5 backdrop-blur-lg border-b border-white/10">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-bold text-white">时光轴</h2>
                  <button
                    onClick={() => setIsOpen(false)}
                    className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                  >
                    <X className="w-6 h-6 text-white" />
                  </button>
                </div>

                {/* 类型筛选 */}
                <div className="flex gap-2">
                  <button
                    onClick={() => setSelectedType('all')}
                    className={`px-3 py-1.5 rounded-lg text-sm transition-all ${
                      selectedType === 'all'
                        ? 'bg-white/20 text-white'
                        : 'bg-white/5 text-white/60 hover:bg-white/10'
                    }`}
                  >
                    全部
                  </button>
                  {Object.entries(typeConfig).map(([type, config]) => {
                    const Icon = config.icon
                    return (
                      <button
                        key={type}
                        onClick={() => setSelectedType(type as RecordType)}
                        className={`px-3 py-1.5 rounded-lg text-sm transition-all flex items-center gap-1 ${
                          selectedType === type
                            ? 'bg-white/20 text-white'
                            : 'bg-white/5 text-white/60 hover:bg-white/10'
                        }`}
                      >
                        <Icon className="w-4 h-4" />
                        {config.label}
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* 记录列表 */}
              <div className="overflow-y-auto h-[calc(100%-140px)] p-4 space-y-3">
                {filteredRecords.length === 0 ? (
                  <div className="text-center py-12 text-white/40">
                    <Calendar className="w-12 h-12 mx-auto mb-3 opacity-50" />
                    <p>还没有记录</p>
                    <p className="text-sm mt-1">开始记录你的心情和想法吧</p>
                  </div>
                ) : (
                  filteredRecords.map((record) => {
                    const config = typeConfig[record.type]
                    const Icon = config.icon
                    const isExpanded = expandedId === record.id

                    return (
                      <motion.div
                        key={record.id}
                        layout
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`${config.bg} backdrop-blur-sm rounded-xl p-4 border border-white/10 cursor-pointer hover:border-white/20 transition-all`}
                        onClick={() => setExpandedId(isExpanded ? null : record.id)}
                      >
                        {/* 头部 */}
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <Icon className={`w-5 h-5 ${config.color}`} />
                            <span className={`text-sm font-semibold ${config.color}`}>
                              {config.label}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-white/50">
                              {formatDate(record.created_at)}
                            </span>
                            <ChevronDown
                              className={`w-4 h-4 text-white/50 transition-transform ${
                                isExpanded ? 'rotate-180' : ''
                              }`}
                            />
                          </div>
                        </div>

                        {/* 关键信息 */}
                        {record.emotion && (
                          <div className="text-sm text-white/70 mb-2">
                            💫 {record.emotion.primary_emotion}
                          </div>
                        )}
                        {record.keywords && record.keywords.length > 0 && (
                          <div className="text-sm text-white/70 mb-2">
                            ✨ {record.keywords.join(', ')}
                          </div>
                        )}
                        {record.theme && (
                          <div className="text-sm text-white/70 mb-2">
                            🌳 {record.theme}
                          </div>
                        )}

                        {/* 内容预览/完整内容 */}
                        <AnimatePresence>
                          {isExpanded ? (
                            <motion.div
                              initial={{ height: 0, opacity: 0 }}
                              animate={{ height: 'auto', opacity: 1 }}
                              exit={{ height: 0, opacity: 0 }}
                              className="text-white/90 text-sm leading-relaxed mt-3 pt-3 border-t border-white/10"
                            >
                              {record.content}
                            </motion.div>
                          ) : (
                            <div className="text-white/60 text-sm line-clamp-2">
                              {record.content}
                            </div>
                          )}
                        </AnimatePresence>
                      </motion.div>
                    )
                  })
                )}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
