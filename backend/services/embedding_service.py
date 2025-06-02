# backend/services/embedding_service.py

import os
import torch
import clip
import faiss
import numpy as np
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

INDEX_FILE = "faiss.index"
PATHS_FILE = "image_paths.txt"
IMAGE_DIR = "../images"

# === Internal Helpers ===

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

# === Main Embedding Function ===

def process_images():
    index, saved_paths = _load_index()
    all_paths = _get_all_image_paths()
    new_paths = [p for p in all_paths if p not in saved_paths]
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
            saved_paths.append(path)
        except Exception as e:
            print(f"[Error] Failed on {path}: {e}")

    _save_index(index, saved_paths)
    return {"indexed": len(new_paths), "total": len(saved_paths), "status": "ok"}

# === Text Search Function ===

def search_images(text_query: str, top_k: int = 3):
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

    D, I = index.search(text_emb.cpu().numpy(), min(top_k, len(image_paths)))
    return [image_paths[i] for i in I[0]]
