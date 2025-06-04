import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .embedding_service import process_images, remove_deleted_image
from .face_grouping_service import process_faces, remove_deleted_face
import os

class ImageHandler(FileSystemEventHandler):
    def __init__(self):
        self.processing_files = set()  # Track files being processed
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def process_with_retry(self, file_path):
        """Process an image with retry logic for both embeddings and faces"""
        if file_path in self.processing_files:
            return  # Skip if already processing this file
            
        self.processing_files.add(file_path)
        retry_count = 0
        
        while retry_count < self.max_retries:
            try:
                print(f"[Watcher] Processing image (attempt {retry_count + 1}/{self.max_retries}): {file_path}")
                # Process both embeddings and faces
                embedding_result = process_images()
                face_result = process_faces()
                
                if embedding_result["status"] == "ok":
                    print(f"[Watcher] Successfully processed image: {file_path}")
                    print(f"[Watcher] Embeddings: {embedding_result}")
                    print(f"[Watcher] Faces: {face_result}")
                    break
                else:
                    print(f"[Watcher] Processing returned status: {embedding_result['status']}")
            except Exception as e:
                print(f"[Watcher] Error processing {file_path} (attempt {retry_count + 1}): {str(e)}")
            
            retry_count += 1
            if retry_count < self.max_retries:
                print(f"[Watcher] Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
        
        self.processing_files.remove(file_path)
        if retry_count == self.max_retries:
            print(f"[Watcher] Failed to process {file_path} after {self.max_retries} attempts")

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"[Watcher] New image detected: {event.src_path}")
            # Wait a short time to ensure file is fully written
            time.sleep(1)
            self.process_with_retry(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"[Watcher] Image deleted: {event.src_path}")
            # Remove from both embeddings and faces
            remove_deleted_image(event.src_path)
            remove_deleted_face(event.src_path)

def start_watching():
    watch_path = os.getenv("IMAGE_DIR", "/app/images")
    print(f"[Watcher] Watching: {watch_path}")
    
    # Retry initialization if directory is not available
    max_retries = 5
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            if not os.path.exists(watch_path):
                print(f"[Watcher] Directory not available, attempt {attempt + 1}/{max_retries}")
                time.sleep(retry_delay)
                continue
            
            event_handler = ImageHandler()
            observer = Observer()
            observer.schedule(event_handler, watch_path, recursive=False)
            observer.start()
            print(f"[Watcher] Successfully started watching {watch_path}")
            return observer
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"[Watcher] Failed to start watcher, retrying in {retry_delay} seconds: {e}")
                time.sleep(retry_delay)
            else:
                print(f"[Watcher] Failed to start watcher after {max_retries} attempts: {e}")
                return None
