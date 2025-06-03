"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import PhotoGrid from "@/components/photo-grid"
import type { Photo } from "@/lib/types"

const API_URL = "http://localhost:8000"

export default function FaceGroupPage() {
  const params = useParams()
  const [photos, setPhotos] = useState<Photo[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFaceGroup = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${API_URL}/face-groups`)
        const data = await response.json()
        
        // Get the images for this face group
        const groupImages = data.clusters[params.id as string] || []
        
        // Transform the images to match the Photo type
        const transformedPhotos: Photo[] = groupImages.map((path: string) => ({
          id: path,
          url: `${API_URL}/images/${encodeURIComponent(path.replace('images/', ''))}`,
          title: path.split('/').pop()?.replace(/\.[^/.]+$/, "") || "",
          date: new Date().toLocaleDateString(),
          height: 300,
        }))

        setPhotos(transformedPhotos)
      } catch (error) {
        console.error("Error fetching face group:", error)
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchFaceGroup()
    }
  }, [params.id])

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-xl text-gray-500 dark:text-gray-400">Loading...</p>
      </div>
    )
  }

  if (photos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-xl text-gray-500 dark:text-gray-400">No photos found in this face group</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-end">
        <p className="text-gray-400 dark:text-gray-400 font-retro">{photos.length} photos</p>
      </div>
      <PhotoGrid photos={photos} />
    </div>
  )
} 