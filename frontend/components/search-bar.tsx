"use client"

import type React from "react"

import { Search, X } from "lucide-react"
import { useRouter, usePathname } from "next/navigation"
import { useState, useEffect } from "react"

export default function SearchBar({ initialQuery = "" }: { initialQuery?: string }) {
  const [query, setQuery] = useState(initialQuery)
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    setQuery(initialQuery)
  }, [initialQuery])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()

    if (query) {
      router.push(`${pathname}?q=${encodeURIComponent(query)}`)
    } else {
      router.push(pathname)
    }
  }

  const clearSearch = () => {
    setQuery("")
    router.push(pathname)
  }

  return (
    <form onSubmit={handleSearch} className="relative">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <Search className="w-5 h-5 text-gray-400" />
        </div>
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="block w-full p-3 pl-10 pr-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Search photos..."
        />
        {query && (
          <button type="button" onClick={clearSearch} className="absolute inset-y-0 right-0 flex items-center pr-3">
            <X className="w-5 h-5 text-gray-400 hover:text-gray-500" />
          </button>
        )}
      </div>
    </form>
  )
}
