from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from services.embedding_service import process_images, search_images
from services.face_grouping_service import group_faces
from services.watcher import start_watching
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the images directory
app.mount("/images", StaticFiles(directory=os.getenv("IMAGE_DIR", "/app/images")), name="images")

# Start the image watcher on app startup
@app.on_event("startup")
def startup_event():
    print("[Startup] Starting image folder watcher...")
    start_watching()

@app.post("/process-images")
def process_route():
    return process_images()

@app.get("/search")
def search_route(q: str = Query(..., alias="q")):
    return {"results": search_images(q)}

@app.get("/face-groups")
def get_face_clusters():
    return group_faces()

@app.get("/health")
def health_check():
    return {"status": "healthy"}