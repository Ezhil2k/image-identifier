"use client"

import { useEffect, useState } from "react"

export default function EmptyState({ message }: { message: string }) {
  const [frame, setFrame] = useState(0)
  const frames = [
    "┌(・。・)┘",
    "└(・。・)┐",
    "┌(・。・)┘",
    "└(・。・)┐",
  ]
  

  useEffect(() => {
    const interval = setInterval(() => {
      setFrame((prev) => (prev + 1) % frames.length)
    }, 500)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex flex-col items-center justify-center h-[calc(100vh-200px)] space-y-3">
      <div className="text-lg font-retro animate-bounce">
        {frames[frame]}
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400 font-retro">{message}</p>
      <div className="w-20 h-1 bg-gradient-to-r from-transparent via-gray-500 to-transparent animate-pulse" />
    </div>
  )
} 