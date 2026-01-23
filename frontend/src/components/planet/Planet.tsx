'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sphere } from '@react-three/drei'
import { Mesh } from 'three'
import { usePlanetStore } from '@/stores/planetStore'
import StarElement from './StarElement'
import TreeElement from './TreeElement'

export default function Planet() {
  const meshRef = useRef<Mesh>(null)
  const cloudRef = useRef<Mesh>(null)
  const { planetState } = usePlanetStore()

  // 星球自转动画 + 云层飘动
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.001
    }
    if (cloudRef.current) {
      cloudRef.current.rotation.y += 0.0015 // 云层转得稍快一点
    }
  })

  // 从颜色字符串获取大气层颜色
  const atmosphereColor = planetState?.atmosphere_color || '#87CEEB'

  return (
    <group>
      {/* 主星球 - 地球风格（蓝绿色） */}
      <Sphere ref={meshRef} args={[1, 64, 64]}>
        <meshStandardMaterial
          color="#3b82f6" // 海洋蓝
          roughness={0.7}
          metalness={0.3}
        />
      </Sphere>

      {/* 陆地层（绿色斑块效果） */}
      <Sphere args={[1.01, 64, 64]}>
        <meshStandardMaterial
          color="#10b981" // 治愈绿
          transparent
          opacity={0.4}
          roughness={0.8}
          metalness={0.1}
        />
      </Sphere>

      {/* 云层 */}
      <Sphere ref={cloudRef} args={[1.08, 32, 32]}>
        <meshStandardMaterial
          color="#ffffff"
          transparent
          opacity={0.2}
          roughness={0.9}
          metalness={0}
        />
      </Sphere>

      {/* 大气层（情感色彩） */}
      <Sphere args={[1.12, 64, 64]}>
        <meshStandardMaterial
          color={atmosphereColor}
          transparent
          opacity={0.25}
          roughness={0.4}
          metalness={0.1}
        />
      </Sphere>

      {/* 渲染星星（灵感） */}
      {planetState?.stars.map((star) => (
        <StarElement key={star.id} data={star} />
      ))}

      {/* 渲染树木（思考） */}
      {planetState?.trees.map((tree) => (
        <TreeElement key={tree.id} data={tree} />
      ))}
    </group>
  )
}
