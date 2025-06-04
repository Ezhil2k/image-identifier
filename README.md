# Image Identifier

A modern web application for organizing and searching through your photo collection using AI-powered image recognition and face detection.

## Features

- **AI-Powered Image Search**: Search images using natural language descriptions
- **Face Detection & Grouping**: Automatically detect and group similar faces
- **Real-time Updates**: Automatic processing of new images
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Docker Support**: Easy deployment with Docker

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.10+ (for backend development)

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/Ezhil2k/image-identifier.git
   cd image_identifier
   ```

2. Create an `images` directory for your photos:
   ```bash
   mkdir images
   ```

3. Start the backend service:
   ```bash
   docker-compose up --build
   ```

4. Start the frontend development server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

### Docker Services

The application uses Docker Compose for containerization:

- **Backend Service**:
  - FastAPI application
  - Runs on port 8000
  - Mounts `./images` directory
  - Includes health checks
  - Auto-restarts unless stopped manually

## Project Structure

```
image_identifier/
├── backend/              # FastAPI backend
│   ├── services/        # Core services (embedding, face detection)
│   ├── main.py         # FastAPI application
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend
│   ├── app/            # Next.js app directory
│   ├── components/     # React components
│   └── package.json    # Node.js dependencies
├── images/             # Photo directory (mounted in Docker)
├── docker-compose.yml  # Docker services configuration
└── README.md          # This file
```

## Usage

1. **Adding Photos**:
   - Place your images in the `images/` directory
   - The backend watcher will automatically process new images
   - Use the refresh button to force immediate processing

2. **Searching Images**:
   - Use the search bar to find images by description
   - Results update in real-time as you type
   - Click on images to view full size

3. **Face Detection**:
   - Navigate to the Faces tab to view grouped faces
   - Click on a face group to see all photos with that person
   - Use the search bar to find specific face groups

## Development

### Backend

The backend is a FastAPI application that provides:
- Image search using CLIP embeddings
- Face detection and grouping
- File system watching for new images

To run the backend in development mode:
```bash
docker-compose up --build
```

### Frontend

The frontend is a Next.js application with:
- Modern React with TypeScript
- Tailwind CSS for styling
- Responsive photo grid
- Face group visualization

To run the frontend in development mode:
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

### Backend
- `IMAGE_DIR`: Directory to watch for images (default: `/app/images`)
- `INDEX_FILE`: Path to FAISS index (default: `/app/faiss.index`)
- `PATHS_FILE`: Path to image paths file (default: `/app/image_paths.txt`)

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: `http://localhost:8000`)

## License

MIT
