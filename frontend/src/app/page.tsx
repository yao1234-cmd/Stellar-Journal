'use client'

import { Suspense, useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/stores/authStore'
import { LogOut } from 'lucide-react'
import PlanetScene from '@/components/planet/PlanetScene'
import RecordPanel from '@/components/ui/RecordPanel'
import RecordDrawer from '@/components/ui/RecordDrawer'
import StatsPanel from '@/components/ui/StatsPanel'
import SplashScreen from '@/components/ui/SplashScreen'

export default function Home() {
  const router = useRouter()
  const { isAuthenticated, clearAuth, user, _hasHydrated } = useAuthStore()
  const [showSplash, setShowSplash] = useState(true)  // 初始就显示动画，避免主界面闪现

  // 启动画面逻辑：3.5 秒后自动隐藏
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowSplash(false)
    }, 3500)
    
    return () => clearTimeout(timer)
  }, [])

  // 路由保护：启动画面结束后再检查认证状态
  useEffect(() => {
    if (_hasHydrated && !isAuthenticated && !showSplash) {
      router.push('/login')
    }
  }, [_hasHydrated, isAuthenticated, showSplash, router])

  const handleLogout = () => {
    clearAuth()
    router.push('/login')
  }

  // 等待 hydration 时显示启动画面
  if (!_hasHydrated) {
    return (
      <>
        <SplashScreen show={showSplash} onComplete={() => setShowSplash(false)} />
        <div className="w-screen h-screen bg-gradient-to-b from-indigo-950 via-purple-900 to-slate-900" />
      </>
    )
  }

  return (
    <>
      {/* 启动画面 */}
      <SplashScreen show={showSplash} onComplete={() => setShowSplash(false)} />
      
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
        <header className="fixed top-0 left-0 right-0 p-6 flex items-center justify-between z-50">
          <div className="glass-effect rounded-2xl px-6 py-3">
            <h1 className="text-2xl font-bold text-white">
              星迹 <span className="text-lg font-normal text-white/70">Stellar Journal</span>
            </h1>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="glass-effect rounded-2xl px-4 py-2 text-white/90 text-sm">
              {user?.username}
            </div>
            <StatsPanel />
            <button
              onClick={handleLogout}
              className="glass-effect rounded-2xl p-3 text-white/80 hover:text-white hover:bg-white/10 transition-all"
              title="登出"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </header>

        {/* 底部记录面板 */}
        <div className="fixed bottom-0 left-0 right-0 p-6">
          <RecordPanel />
        </div>

        {/* 记录抽屉（侧边滑出） */}
        <RecordDrawer />
      </div>
    </main>
    </>
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
