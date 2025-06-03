"use client"

import Image from "next/image"
import Link from "next/link"
import type { FaceAlbum } from "@/lib/types"
import { useState } from "react"

function FaceAlbumCard({ album }: { album: FaceAlbum }) {
  const [error, setError] = useState(false)

  if (error) {
    return null // Don't render anything if image fails to load
  }

  return (
    <Link href={`/faces/${album.id}`} key={album.id} className="group">
      <div className="relative">
        <div className="aspect-square relative overflow-hidden rounded-full border-2 border-white dark:border-gray-800 shadow-md group-hover:shadow-lg transition-all duration-300 group-hover:scale-105 w-32 h-32 mx-auto">
          <Image
            src={album.coverImage || "/placeholder.svg"}
            alt="Face group"
            fill
            sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, (max-width: 1024px) 25vw, 20vw"
            className="object-cover"
            onError={() => setError(true)} // Hide image if it fails to load
          />
        </div>
        <div className="mt-2 text-center">
          {album.name && <h3 className="font-medium truncate text-sm">{album.name}</h3>}
          <p className="text-xs text-gray-500 dark:text-gray-400">{album.count} photos</p>
        </div>
      </div>
    </Link>
  )
}

export default function FacesLibrary({ faceAlbums }: { faceAlbums: FaceAlbum[] }) {
  if (faceAlbums.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-xl text-gray-500 dark:text-gray-400">No face albums found</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-8">
      {faceAlbums.map((album) => (
        <FaceAlbumCard key={album.id} album={album} />
      ))}
    </div>
  )
}
