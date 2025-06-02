import type { Photo, FaceAlbum } from "./types"

const API_URL = "http://localhost:8000"

// Function to get photos with optional search filter
export async function getPhotos(query = ""): Promise<Photo[]> {
  try {
    const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`)
    const data = await response.json()
    
    // Transform the backend response to match our Photo type
    return data.results.map((path: string) => ({
      id: path,
      url: `${API_URL}/images/${encodeURIComponent(path.replace('images/', ''))}`,
      title: path.split('/').pop()?.replace(/\.[^/.]+$/, "") || "",
      date: new Date().toLocaleDateString(),
      height: 300, // Default height, will be adjusted by the image component
    }))
  } catch (error) {
    console.error('Error fetching photos:', error)
    return []
  }
}

// Function to get face albums with optional search filter
export async function getFaceAlbums(query = ""): Promise<FaceAlbum[]> {
  try {
    const response = await fetch(`${API_URL}/face-groups`)
    const data = await response.json() as { clusters: Record<string, string[]> }
    
    // Transform the clusters into face albums
    return Object.entries(data.clusters).map(([id, images]) => ({
      id,
      name: "",  // Empty name since we don't want any labels
      coverImage: `${API_URL}/images/${encodeURIComponent(images[0].replace('images/', ''))}`,
      count: images.length,
    }))
  } catch (error) {
    console.error('Error fetching face albums:', error)
    return []
  }
}

// Function to process new images
export async function processImages(): Promise<{ indexed: number; total: number; status: string }> {
  try {
    const response = await fetch(`${API_URL}/process-images`, {
      method: 'POST',  // Explicitly set method to POST
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Error processing images:', error)
    throw error
  }
}
