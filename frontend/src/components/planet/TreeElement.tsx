'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { Cone, Sphere, Html } from '@react-three/drei'
import { Vector3, Group } from 'three'
import { TreeElement as TreeData } from '@/lib/api'

interface TreeElementProps {
  data: TreeData
}

export default function TreeElement({ data }: TreeElementProps) {
  const groupRef = useRef<Group>(null)
  const [hovered, setHovered] = useState(false)

  // 获取位置数据
  const position = new Vector3(
    data.position.x || 0,
    data.position.y || 0,
    data.position.z || 0
  )

  // 树的尺寸
  const trunkHeight = data.size * 0.4
  const crownRadius = data.size * 0.35

  // 轻微摇摆动画
  useFrame(({ clock }) => {
    if (groupRef.current) {
      const time = clock.getElapsedTime()
      groupRef.current.rotation.z = Math.sin(time * 0.5 + data.position.x * 5) * 0.05
    }
  })

  return (
    <group
      ref={groupRef}
      position={position}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
    >
      {/* 树干 */}
      <Cone args={[0.025, trunkHeight, 8]} position={[0, trunkHeight / 2, 0]}>
        <meshStandardMaterial color="#8b5a3c" roughness={0.9} metalness={0.1} />
      </Cone>

      {/* 树冠 - 三层叠加营造层次感 */}
      {/* 底层 */}
      <Sphere 
        args={[crownRadius, 16, 16]} 
        position={[0, trunkHeight + crownRadius * 0.5, 0]}
      >
        <meshStandardMaterial
          color="#34d399" // 治愈绿
          roughness={0.85}
          metalness={0.05}
          emissive={hovered ? '#10b981' : '#000000'}
          emissiveIntensity={hovered ? 0.4 : 0}
        />
      </Sphere>

      {/* 中层 */}
      <Sphere 
        args={[crownRadius * 0.7, 14, 14]} 
        position={[0, trunkHeight + crownRadius * 0.9, 0]}
      >
        <meshStandardMaterial
          color="#22c55e" // 稍深的绿
          roughness={0.8}
          metalness={0.05}
        />
      </Sphere>

      {/* 顶层 */}
      <Sphere 
        args={[crownRadius * 0.4, 12, 12]} 
        position={[0, trunkHeight + crownRadius * 1.2, 0]}
      >
        <meshStandardMaterial
          color="#4ade80" // 明亮绿
          roughness={0.75}
          metalness={0.05}
        />
      </Sphere>

      {/* 悬停时显示主题和叶子数 */}
      {hovered && (
        <Html position={[0, trunkHeight + crownRadius * 1.7, 0]}>
          <div className="bg-gradient-to-br from-green-500/90 to-emerald-600/90 text-white px-4 py-2 rounded-xl text-sm whitespace-nowrap shadow-xl backdrop-blur-sm">
            <div className="font-bold flex items-center gap-1">
              🌳 {data.theme}
            </div>
            <div className="text-xs text-green-100 mt-0.5">{data.leaf_count} 条思考枝叶</div>
          </div>
        </Html>
      )}
    </group>
  )
}
