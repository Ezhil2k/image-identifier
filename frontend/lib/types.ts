export interface Photo {
  id: string
  url: string
  title?: string
  date?: string
  height: number
}

export interface FaceAlbum {
  id: string
  name: string
  coverImage: string
  count: number
}
