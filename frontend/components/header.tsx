"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Menu, Moon, Sun, RefreshCw } from "lucide-react"
import { useState, useEffect } from "react"
import { processImages } from "@/lib/photo-service"

export default function Header() {
  const pathname = usePathname()
  const [darkMode, setDarkMode] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)

  useEffect(() => {
    // Check for dark mode preference
    if (typeof window !== "undefined") {
      const isDarkMode =
        localStorage.getItem("darkMode") === "true" || window.matchMedia("(prefers-color-scheme: dark)").matches

      setDarkMode(isDarkMode)
      if (isDarkMode) {
        document.documentElement.classList.add("dark")
      }
    }
  }, [])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    if (typeof window !== "undefined") {
      localStorage.setItem("darkMode", (!darkMode).toString())
      document.documentElement.classList.toggle("dark")
    }
  }

  const handleRefresh = async () => {
    if (isRefreshing) return
    setIsRefreshing(true)
    try {
      const result = await processImages()
      console.log("Processed images:", result)
      // Trigger a page reload to show new images
      window.location.reload()
    } catch (error) {
      console.error("Error refreshing images:", error)
    } finally {
      setIsRefreshing(false)
    }
  }

  const navItems = [
    { name: "PHOTOS", path: "/" },
    { name: "FACES", path: "/faces" },
  ]

  return (
    <header className="bg-black text-white p-4 border-b-2 border-gray-700" style={{ borderColor: 'rgba(var(--border-color), 0.8)' }}>
      <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-4">
          <Link href="/" className="font-bold text-white" style={{ fontSize: '0.85rem' }}>
            <span className="font-retro" style={{ fontSize: '0.85rem' }}>RETRO GALLERY</span>
            </Link>
          <span className="mx-2 text-gray-600 font-retro" style={{ fontSize: '0.85rem' }}>|</span>
          <nav>
            <ul className="flex space-x-4">
              {navItems.map((item) => (
                <li key={item.path}>
                <Link
                  href={item.path}
                    className={`font-retro ${pathname === item.path ? 'text-white border-b-2 border-white' : 'text-gray-400 hover:text-white'}`}
                    style={{ fontSize: '0.65rem', letterSpacing: '0.05em' }}
                >
                  {item.name}
                </Link>
                </li>
              ))}
            </ul>
            </nav>
          </div>
        <div className="flex items-center space-x-4">
            <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className={`font-retro text-sm p-1 border-2 border-white text-white hover:bg-gray-800 hover:border-white transition-colors duration-200 rounded-full ${
              isRefreshing ? 'opacity-50 cursor-not-allowed' : ''
            }`}
            aria-label="Refresh images"
            title="Process new images"
          >
            <RefreshCw size={16} />
            </button>

            <button
            onClick={toggleDarkMode}
            className="font-retro text-sm p-1 border-2 border-white text-white hover:bg-gray-800 hover:border-white transition-colors duration-200 rounded-full"
            aria-label="Toggle dark mode"
            >
            {darkMode ? <Sun size={16} /> : <Moon size={16} />}
            </button>
        </div>
      </div>
    </header>
  )
}
