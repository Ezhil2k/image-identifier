"use client"

import { useEffect, useState } from "react"
import { useSearchParams } from "next/navigation"
import SearchBar from "@/components/search-bar"
import FacesLibrary from "@/components/faces-library"
import { getFaceAlbums } from "@/lib/photo-service"
import type { FaceAlbum } from "@/lib/types"

export default function FacesPage() {
  const [faceAlbums, setFaceAlbums] = useState<FaceAlbum[]>([])
  const searchParams = useSearchParams()
  const [query, setQuery] = useState("")

  // Update query when searchParams changes
  useEffect(() => {
    const newQuery = searchParams.get("q") || ""
    if (newQuery !== query) {
      setQuery(newQuery)
    }
  }, [searchParams, query])

  const fetchFaceAlbums = async () => {
    try {
      const newAlbums = await getFaceAlbums(query)
      setFaceAlbums(newAlbums)
    } catch (error) {
      console.error("Error fetching face albums:", error)
      // Keep existing albums on error
    }
  }

  // Initial fetch
  useEffect(() => {
    fetchFaceAlbums()
  }, [query])

  // Poll for updates every 10 seconds
  useEffect(() => {
    const interval = setInterval(fetchFaceAlbums, 10000)
    return () => clearInterval(interval)
  }, [query])

  return (
    <div className="space-y-6">
      <SearchBar initialQuery={query} />
      <FacesLibrary faceAlbums={faceAlbums} />
    </div>
  )
}
