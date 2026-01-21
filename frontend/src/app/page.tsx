'use client'

import { Suspense } from 'react'
import PlanetScene from '@/components/planet/PlanetScene'
import RecordPanel from '@/components/ui/RecordPanel'
import RecordDrawer from '@/components/ui/RecordDrawer'
import StatsPanel from '@/components/ui/StatsPanel'

export default function Home() {
  return (
    <main className="relative w-screen h-screen overflow-hidden bg-gradient-to-b from-indigo-950 via-purple-900 to-slate-900">
      {/* 3D 星球场景 */}
      <div className="canvas-container">
        <Suspense fallback={<LoadingFallback />}>
          <PlanetScene />
        </Suspense>
      </div>

      {/* UI 覆层 */}
      <div className="ui-overlay">
        {/* 顶部标题栏 */}
        <header className="fixed top-0 left-0 right-0 p-6 flex items-center justify-between">
          <div className="glass-effect rounded-2xl px-6 py-3">
            <h1 className="text-2xl font-bold text-white">
              星迹 <span className="text-lg font-normal text-white/70">Stellar Journal</span>
            </h1>
          </div>
          
          <StatsPanel />
        </header>

        {/* 底部记录面板 */}
        <div className="fixed bottom-0 left-0 right-0 p-6">
          <RecordPanel />
        </div>

        {/* 记录抽屉（侧边滑出） */}
        <RecordDrawer />
      </div>
    </main>
  )
}

function LoadingFallback() {
  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="text-white text-xl">
        <div className="animate-pulse">加载星球中...</div>
      </div>
    </div>
  )
}
