import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .embedding_service import process_images, remove_deleted_image
import os

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"[Watcher] New image detected: {event.src_path}")
            process_images()

    def on_deleted(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"[Watcher] Image deleted: {event.src_path}")
            remove_deleted_image(event.src_path)

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
                # Don't raise the error, let the application continue running
                return None
