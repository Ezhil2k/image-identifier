import SearchBar from "@/components/search-bar"
import PhotoGrid from "@/components/photo-grid"
import { getPhotos } from "@/lib/photo-service"

export default async function HomePage({
  searchParams,
}: {
  searchParams: { q?: string }
}) {
  const query = searchParams.q || ""
  const photos = await getPhotos(query)

  return (
    <div className="space-y-6">
      <SearchBar initialQuery={query} />
      <PhotoGrid photos={photos} />
    </div>
  )
}
