'use client'

import { useRef, useState } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sphere, Html } from '@react-three/drei'
import { Mesh, Vector3 } from 'three'
import { StarElement as StarData } from '@/lib/api'

interface StarElementProps {
  data: StarData
}

export default function StarElement({ data }: StarElementProps) {
  const meshRef = useRef<Mesh>(null)
  const glowRef = useRef<Mesh>(null)
  const [hovered, setHovered] = useState(false)

  // 获取位置数据
  const position = new Vector3(
    data.position.x || 0,
    data.position.y || 0,
    data.position.z || 0
  )

  // 公转动画 + 闪烁效果
  useFrame(({ clock }) => {
    const time = clock.getElapsedTime()
    
    // 公转
    if (meshRef.current && data.position.orbit_radius) {
      const angle = (data.position.orbit_angle || 0) * (Math.PI / 180) + time * 0.2
      const radius = data.position.orbit_radius
      
      meshRef.current.position.x = radius * Math.cos(angle)
      meshRef.current.position.z = radius * Math.sin(angle)
      meshRef.current.position.y = data.position.y || 0
      
      // 光晕同步位置
      if (glowRef.current) {
        glowRef.current.position.copy(meshRef.current.position)
      }
    }
    
    // 闪烁效果
    if (meshRef.current) {
      const twinkle = Math.sin(time * 3 + data.position.x * 10) * 0.3 + 0.7
      meshRef.current.scale.setScalar(twinkle)
    }
  })

  return (
    <group>
      {/* 星星光晕 */}
      <Sphere
        ref={glowRef}
        args={[data.size * 2, 16, 16]}
        position={position}
      >
        <meshBasicMaterial
          color={data.color}
          transparent
          opacity={0.15}
        />
      </Sphere>

      {/* 星星主体 */}
      <Sphere
        ref={meshRef}
        args={[data.size, 8, 8]}
        position={position}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <meshStandardMaterial
          color={data.color}
          emissive={data.color}
          emissiveIntensity={hovered ? 2 : 1.2}
          metalness={0.9}
          roughness={0.1}
        />
      </Sphere>

      {/* 悬停时显示关键词 */}
      {hovered && (
        <Html position={position}>
          <div className="bg-gradient-to-r from-yellow-400/90 to-orange-400/90 text-white px-3 py-1.5 rounded-lg text-sm whitespace-nowrap shadow-lg backdrop-blur-sm">
            ✨ {data.keyword}
          </div>
        </Html>
      )}
    </group>
  )
}
