import Image from "next/image"
import type { Photo } from "@/lib/types"

export default function PhotoGrid({ photos }: { photos: Photo[] }) {
  if (photos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-xl text-gray-500 dark:text-gray-400">No photos found</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {photos.map((photo) => (
        <div
          key={photo.id}
          className="relative group aspect-square overflow-hidden rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
        >
          <Image
            src={photo.url || "/placeholder.svg"}
            alt={photo.title || "Photo"}
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw"
            className="object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end">
            <div className="p-4 w-full">
              {photo.title && <h3 className="text-white font-medium truncate">{photo.title}</h3>}
              {photo.date && <p className="text-gray-200 text-sm">{photo.date}</p>}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
