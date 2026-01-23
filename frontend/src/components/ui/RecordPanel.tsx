'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Heart, Sparkles, MessageSquare, Mic, Send } from 'lucide-react'
import { useRecordStore } from '@/stores/recordStore'
import { usePlanetStore } from '@/stores/planetStore'

type RecordType = 'mood' | 'spark' | 'thought'

const recordTypes = [
  { type: 'mood' as RecordType, label: '心情', icon: Heart, color: 'text-pink-400' },
  { type: 'spark' as RecordType, label: '灵感', icon: Sparkles, color: 'text-yellow-400' },
  { type: 'thought' as RecordType, label: '思考', icon: MessageSquare, color: 'text-green-400' },
]

export default function RecordPanel() {
  const [selectedType, setSelectedType] = useState<RecordType>('mood')
  const [content, setContent] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  
  const { createRecord, loading } = useRecordStore()
  const { refreshPlanet } = usePlanetStore()

  const handleSubmit = async () => {
    if (!content.trim()) {
      return
    }

    const result = await createRecord({
      type: selectedType,
      content: content.trim(),
    })

    if (result) {
      setContent('')
      await refreshPlanet()
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <motion.div
      initial={{ y: 100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="glass-effect rounded-3xl p-6 max-w-2xl mx-auto"
    >
      {/* 类型选择 */}
      <div className="flex gap-3 mb-4">
        {recordTypes.map(({ type, label, icon: Icon, color }) => (
          <button
            key={type}
            onClick={() => setSelectedType(type)}
            className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl transition-all ${
              selectedType === type
                ? 'bg-white/20 shadow-lg scale-105'
                : 'bg-white/5 hover:bg-white/10'
            }`}
          >
            <Icon className={`w-5 h-5 ${selectedType === type ? color : 'text-white/50'}`} />
            <span className={selectedType === type ? 'text-white font-medium' : 'text-white/70'}>
              {label}
            </span>
          </button>
        ))}
      </div>

      {/* 输入区域 */}
      <div className="relative">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={getPlaceholder(selectedType)}
          className="w-full bg-white/10 text-white placeholder-white/40 rounded-xl px-4 py-3 pr-24 resize-none focus:outline-none focus:ring-2 focus:ring-white/30 transition-all"
          rows={3}
          disabled={loading}
        />

        {/* 操作按钮 */}
        <div className="absolute bottom-3 right-3 flex gap-2">
          {/* 语音按钮 */}
          <button
            onClick={() => setIsRecording(!isRecording)}
            className={`p-2 rounded-lg transition-all ${
              isRecording
                ? 'bg-red-500 text-white pulse-glow'
                : 'bg-white/10 text-white/70 hover:bg-white/20'
            }`}
            disabled={loading}
          >
            <Mic className="w-5 h-5" />
          </button>

          {/* 发送按钮 */}
          <button
            onClick={handleSubmit}
            disabled={!content.trim() || loading}
            className="p-2 rounded-lg bg-stellar-500 text-white hover:bg-stellar-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* 提示文本 */}
      <AnimatePresence>
        {selectedType === 'mood' && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-3 text-sm text-white/60"
          >
            💜 分享你的心情，让星球展现你的情绪色彩
          </motion.p>
        )}
        {selectedType === 'spark' && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-3 text-sm text-white/60"
          >
            ✨ 记录你的灵感，它将化为环绕星球的星辰
          </motion.p>
        )}
        {selectedType === 'thought' && (
          <motion.p
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-3 text-sm text-white/60"
          >
            🌳 沉淀你的思考，让它成为星球上的生命之树
          </motion.p>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

function getPlaceholder(type: RecordType): string {
  switch (type) {
    case 'mood':
      return '此刻的心情如何？分享你的感受...'
    case 'spark':
      return '捕捉灵光一闪的瞬间...'
    case 'thought':
      return '记录深度思考...'
  }
}
