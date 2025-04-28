"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Menu, Moon, Sun } from "lucide-react"
import { useState, useEffect } from "react"

export default function Header() {
  const pathname = usePathname()
  const [darkMode, setDarkMode] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

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

  const navItems = [
    { name: "Photos", path: "/" },
    { name: "Faces", path: "/faces" },
  ]

  return (
    <header className="sticky top-0 z-10 bg-white dark:bg-gray-800 shadow-sm">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/" className="text-xl font-bold">
              Photo Gallery
            </Link>

            <nav className="hidden md:flex items-center space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  href={item.path}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname === item.path ? "bg-gray-100 dark:bg-gray-700" : "hover:bg-gray-100 dark:hover:bg-gray-700"
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
              aria-label="Toggle dark mode"
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>

            <button
              className="md:hidden p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              <Menu size={20} />
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <nav className="md:hidden mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  pathname === item.path ? "bg-gray-100 dark:bg-gray-700" : "hover:bg-gray-100 dark:hover:bg-gray-700"
                }`}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        )}
      </div>
    </header>
  )
}
