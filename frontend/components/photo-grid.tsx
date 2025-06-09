"use client"

import Image from "next/image"
import type { Photo } from "@/lib/types"
import { useState } from "react"
import EmptyState from "./empty-state"

function PhotoCard({ photo }: { photo: Photo }) {
  const [error, setError] = useState(false)

  if (error) {
    return null // Don't render anything if image fails to load
  }

  return (
    <div
      key={photo.id}
      className="relative group aspect-square overflow-hidden rounded-lg border-2 border-gray-700 shadow-md hover:shadow-lg transition-shadow duration-300 w-40 h-40 mx-auto"
      style={{ borderColor: 'rgba(var(--border-color), 0.8)' }}
    >
      <Image
        src={photo.url || "/placeholder.svg"}
        alt={photo.title || "Photo"}
        fill
        sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, (max-width: 1024px) 25vw, 20vw"
        className="object-cover transition-transform duration-300 group-hover:scale-105"
        onError={() => setError(true)} // Hide image if it fails to load
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black/90 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
        <div className="p-2 w-full">
          {photo.title && <h3 className="text-white font-retro truncate text-[0.6rem]">{photo.title}</h3>}
          {photo.date && <p className="text-gray-400 font-retro text-[0.5rem]">{photo.date}</p>}
        </div>
      </div>
    </div>
  )
}

export default function PhotoGrid({ photos }: { photos: Photo[] }) {
  if (photos.length === 0) {
    return <EmptyState message="No photos found" />
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 2xl:grid-cols-10 gap-6">
      {photos.map((photo) => (
        <PhotoCard key={photo.id} photo={photo} />
      ))}
    </div>
  )
}
