import SearchBar from "@/components/search-bar"
import FacesLibrary from "@/components/faces-library"
import { getFaceAlbums } from "@/lib/photo-service"

export default async function FacesPage({
  searchParams,
}: {
  searchParams: { q?: string }
}) {
  const { q } = await searchParams
  const query = q || ""
  const faceAlbums = await getFaceAlbums(query)

  return (
    <div className="space-y-6">
      <SearchBar initialQuery={query} />
      <FacesLibrary faceAlbums={faceAlbums} />
    </div>
  )
}
