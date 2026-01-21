'use client'

import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import Planet from './Planet'
import { usePlanetStore } from '@/stores/planetStore'
import { useEffect } from 'react'

export default function PlanetScene() {
  const { fetchPlanetState, fetchStats } = usePlanetStore()

  useEffect(() => {
    // 初始加载星球状态
    fetchPlanetState()
    fetchStats()
  }, [fetchPlanetState, fetchStats])

  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 50 }}
      gl={{ antialias: true, alpha: true }}
    >
      {/* 环境光 */}
      <ambientLight intensity={0.5} />
      
      {/* 主光源 */}
      <directionalLight position={[10, 10, 5]} intensity={1} />
      
      {/* 点光源 */}
      <pointLight position={[-10, -10, -5]} intensity={0.5} color="#a78bfa" />

      {/* 星空背景 */}
      <Stars
        radius={100}
        depth={50}
        count={5000}
        factor={4}
        saturation={0}
        fade
        speed={0.5}
      />

      {/* 主星球 */}
      <Planet />

      {/* 轨道控制器 */}
      <OrbitControls
        enablePan={false}
        enableZoom={true}
        minDistance={3}
        maxDistance={10}
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
      />
    </Canvas>
  )
}
