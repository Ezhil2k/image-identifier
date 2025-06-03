"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import SearchBar from "@/components/search-bar"
import PhotoGrid from "@/components/photo-grid"
import { getPhotos } from "@/lib/photo-service"
import type { Photo } from "@/lib/types"

export default function HomePage() {
  const [photos, setPhotos] = useState<Photo[]>([])
  const searchParams = useSearchParams()
  const [query, setQuery] = useState("")

  // Update query when searchParams changes
  useEffect(() => {
    const newQuery = searchParams.get("q") || ""
    if (newQuery !== query) {
      setQuery(newQuery)
    }
  }, [searchParams, query])

  const fetchPhotos = async () => {
    try {
      const newPhotos = await getPhotos(query)
      setPhotos(newPhotos)
    } catch (error) {
      console.error("Error fetching photos:", error)
      // Keep existing photos on error
    }
  }

  // Initial fetch
  useEffect(() => {
    fetchPhotos()
  }, [query])

  // Poll for updates every 10 seconds
  useEffect(() => {
    const interval = setInterval(fetchPhotos, 10000)
    return () => clearInterval(interval)
  }, [query])

  return (
    <div className="space-y-6">
      <SearchBar initialQuery={query} />
      <PhotoGrid photos={photos} />
    </div>
  )
}
