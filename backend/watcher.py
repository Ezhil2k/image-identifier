from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from services.embedding_service import process_images
import time
import threading
import os

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.png', '.jpeg')):
            print(f"[Watcher] New image detected: {event.src_path}")
            process_images()

def start_watching(path="images"):
    path = os.path.abspath(path)  # ensure full path
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer_thread = threading.Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()
    print(f"[Watcher] Watching: {path}")
