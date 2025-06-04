"use client"

import type React from "react"

import { Search, X } from "lucide-react"
import { useRouter, usePathname } from "next/navigation"
import { useState, useEffect } from "react"

const SearchBar = ({ initialQuery = '' }: { initialQuery?: string }) => {
  const router = useRouter()
  const pathname = usePathname()
  const [query, setQuery] = useState(initialQuery)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // Navigate to the current path with the new query parameter
      router.push(`${pathname}?q=${encodeURIComponent(query)}`)
  }

  return (
    <form onSubmit={handleSearch} className="w-full max-w-xl mx-auto">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} /> {/* Icon color */}
        <input
          type="text"
          placeholder="Search for images..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full py-2 pl-10 pr-4 bg-gray-900 text-white border-2 border-gray-700 rounded-lg focus:outline-none focus:border-white font-retro text-[0.65rem]"
        />
      </div>
    </form>
  )
}

export default SearchBar
