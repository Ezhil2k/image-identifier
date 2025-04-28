import Image from "next/image"
import Link from "next/link"
import type { FaceAlbum } from "@/lib/types"

export default function FacesLibrary({ faceAlbums }: { faceAlbums: FaceAlbum[] }) {
  if (faceAlbums.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <p className="text-xl text-gray-500 dark:text-gray-400">No face albums found</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
      {faceAlbums.map((album) => (
        <Link href={`/faces/${album.id}`} key={album.id} className="group">
          <div className="aspect-square relative overflow-hidden rounded-full border-2 border-white dark:border-gray-800 shadow-md group-hover:shadow-lg transition-all duration-300 group-hover:scale-105">
            <Image
              src={album.coverImage || "/placeholder.svg"}
              alt={album.name}
              fill
              sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, (max-width: 1024px) 25vw, 20vw"
              className="object-cover"
            />
          </div>
          <h3 className="mt-3 text-center font-medium truncate">{album.name}</h3>
          <p className="text-center text-sm text-gray-500 dark:text-gray-400">{album.count} photos</p>
        </Link>
      ))}
    </div>
  )
}
