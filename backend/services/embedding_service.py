# backend/services/embedding_service.py

import os
import torch
import clip
import faiss
import numpy as np
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Use environment variables for file paths
INDEX_FILE = os.getenv("INDEX_FILE", "/app/faiss.index")
PATHS_FILE = os.getenv("PATHS_FILE", "/app/image_paths.txt")
IMAGE_DIR = os.getenv("IMAGE_DIR", "/app/images")

# === Internal Helpers ===

def _get_relative_path(absolute_path: str) -> str:
    """Convert absolute path to relative path for the index."""
    # Get just the filename from the path
    return os.path.basename(absolute_path)

def _get_absolute_path(relative_path: str) -> str:
    """Convert relative path to absolute path for file operations."""
    return os.path.join(IMAGE_DIR, relative_path)

def _load_index():
    if os.path.exists(INDEX_FILE) and os.path.exists(PATHS_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(PATHS_FILE, "r") as f:
            paths = [line.strip() for line in f.readlines()]
        return index, paths
    else:
        return faiss.IndexFlatIP(512), []

def _save_index(index, paths):
    faiss.write_index(index, INDEX_FILE)
    with open(PATHS_FILE, "w") as f:
        f.write("\n".join(paths))

def _get_all_image_paths():
    return [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

def _rebuild_index():
    """Rebuild the index from scratch using only existing images"""
    print("[Embedding] Rebuilding index from existing images...")
    all_paths = _get_all_image_paths()
    if not all_paths:
        # If no images exist, create empty index
        index = faiss.IndexFlatIP(512)
        _save_index(index, [])
        return

    # Create new index
    index = faiss.IndexFlatIP(512)
    valid_paths = []
    
    for path in all_paths:
        try:
            img = Image.open(path).convert("RGB")
            img_tensor = preprocess(img).unsqueeze(0).to(device)
            with torch.no_grad():
                emb = model.encode_image(img_tensor).cpu().numpy()
            index.add(emb)
            # Store only the filename in the index
            valid_paths.append(_get_relative_path(path))
        except Exception as e:
            print(f"[Error] Failed to process {path}: {e}")

    _save_index(index, valid_paths)
    print(f"[Embedding] Rebuilt index with {len(valid_paths)} images")

def remove_deleted_image(deleted_path: str):
    """Remove a deleted image from the index and paths file"""
    index, paths = _load_index()
    if not paths:
        return

    # Convert the deleted path to relative path
    relative_path = _get_relative_path(deleted_path)
    
    # Find the index of the deleted path
    try:
        deleted_idx = paths.index(relative_path)
        # Remove the path
        paths.pop(deleted_idx)
        
        # Rebuild the index since FAISS doesn't support direct removal
        _rebuild_index()
        print(f"[Embedding] Removed deleted image: {relative_path}")
    except ValueError:
        # Path wasn't in the index, nothing to do
        print(f"[Embedding] Path not found in index: {relative_path}")
        pass

def process_images():
    index, saved_paths = _load_index()
    all_paths = _get_all_image_paths()
    # Convert saved paths to absolute for comparison
    saved_abs_paths = [_get_absolute_path(p) for p in saved_paths]
    new_paths = [p for p in all_paths if p not in saved_abs_paths]
    if not new_paths:
        return {"indexed": 0, "total": len(saved_paths), "status": "no new images"}

    print(f"[Embedding] Indexing {len(new_paths)} new image(s)...")
    new_images = []
    for path in new_paths:
        try:
            img = Image.open(path).convert("RGB")
            img_tensor = preprocess(img).unsqueeze(0).to(device)
            with torch.no_grad():
                emb = model.encode_image(img_tensor).cpu().numpy()
            index.add(emb)
            # Store only the filename in the index
            saved_paths.append(_get_relative_path(path))
        except Exception as e:
            print(f"[Error] Failed on {path}: {e}")

    _save_index(index, saved_paths)
    return {"indexed": len(new_paths), "total": len(saved_paths), "status": "ok"}

def search_images(text_query: str):
    index, image_paths = _load_index()
    if index.ntotal == 0:
        return []

    # If no query is provided, return all images
    if not text_query.strip():
        return image_paths

    tokens = clip.tokenize([text_query]).to(device)
    with torch.no_grad():
        text_emb = model.encode_text(tokens)
        text_emb /= text_emb.norm(dim=-1, keepdim=True)

    # Search all images
    D, I = index.search(text_emb.cpu().numpy(), len(image_paths))
    return [image_paths[i] for i in I[0]]
