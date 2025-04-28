import type { Photo, FaceAlbum } from "./types"

// Mock data for photos
const mockPhotos: Photo[] = [
  {
    id: "1",
    url: "/placeholder.svg?height=300&width=400",
    title: "Beach Sunset",
    date: "April 15, 2023",
    height: 300,
  },
  {
    id: "2",
    url: "/placeholder.svg?height=400&width=400",
    title: "Mountain View",
    date: "March 22, 2023",
    height: 400,
  },
  {
    id: "3",
    url: "/placeholder.svg?height=250&width=400",
    title: "City Skyline",
    date: "February 10, 2023",
    height: 250,
  },
  {
    id: "4",
    url: "/placeholder.svg?height=350&width=400",
    title: "Forest Trail",
    date: "January 5, 2023",
    height: 350,
  },
  {
    id: "5",
    url: "/placeholder.svg?height=280&width=400",
    title: "Lake Reflection",
    date: "December 12, 2022",
    height: 280,
  },
  {
    id: "6",
    url: "/placeholder.svg?height=320&width=400",
    title: "Desert Landscape",
    date: "November 8, 2022",
    height: 320,
  },
  {
    id: "7",
    url: "/placeholder.svg?height=360&width=400",
    title: "Autumn Colors",
    date: "October 20, 2022",
    height: 360,
  },
  {
    id: "8",
    url: "/placeholder.svg?height=290&width=400",
    title: "Snowy Peaks",
    date: "September 15, 2022",
    height: 290,
  },
]

// Mock data for face albums
const mockFaceAlbums: FaceAlbum[] = [
  {
    id: "face1",
    name: "John",
    coverImage: "/placeholder.svg?height=200&width=200",
    count: 24,
  },
  {
    id: "face2",
    name: "Sarah",
    coverImage: "/placeholder.svg?height=200&width=200",
    count: 18,
  },
  {
    id: "face3",
    name: "Michael",
    coverImage: "/placeholder.svg?height=200&width=200",
    count: 32,
  },
  {
    id: "face4",
    name: "Emily",
    coverImage: "/placeholder.svg?height=200&width=200",
    count: 15,
  },
  {
    id: "face5",
    name: "David",
    coverImage: "/placeholder.svg?height=200&width=200",
    count: 27,
  },
  {
    id: "face6",
    name: "Jessica",
    coverImage: "/placeholder.svg?height=200&width=200",
    count: 21,
  },
]

// Function to get photos with optional search filter
export async function getPhotos(query = ""): Promise<Photo[]> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 500))

  if (!query) {
    return mockPhotos
  }

  // Filter photos based on query
  return mockPhotos.filter((photo) => photo.title?.toLowerCase().includes(query.toLowerCase()))
}

// Function to get face albums with optional search filter
export async function getFaceAlbums(query = ""): Promise<FaceAlbum[]> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 500))

  if (!query) {
    return mockFaceAlbums
  }

  // Filter face albums based on query
  return mockFaceAlbums.filter((album) => album.name.toLowerCase().includes(query.toLowerCase()))
}
