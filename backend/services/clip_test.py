import os
import torch
import clip
import faiss
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# === Config ===
device = "cuda" if torch.cuda.is_available() else "cpu"
INDEX_FILE = "faiss.index"
PATHS_FILE = "image_paths.txt"
IMAGE_DIR = "images"

# === Load CLIP Model ===
print(f"[INFO] Loading CLIP model on: {device}")
model, preprocess = clip.load("ViT-B/32", device=device)

# === Load Image Files ===
def load_images_from_folder(folder_path):
    print(f"[INFO] Loading images from: {folder_path}")
    image_paths = [os.path.join(folder_path, f)
                   for f in os.listdir(folder_path)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images = [(Image.open(path).convert("RGB"), path) for path in image_paths]
    print(f"[INFO] Found {len(images)} images.")
    return images

# === Save/Load FAISS Index & Image Paths ===
def save_index(index, paths):
    print("[INFO] Saving FAISS index and image paths to disk...")
    faiss.write_index(index, INDEX_FILE)
    with open(PATHS_FILE, "w") as f:
        for path in paths:
            f.write(path + "\n")

def load_index():
    print("[INFO] Loading FAISS index and image paths from disk...")
    index = faiss.read_index(INDEX_FILE)
    with open(PATHS_FILE, "r") as f:
        paths = [line.strip() for line in f.readlines()]
    print(f"[INFO] Loaded index with {len(paths)} entries.")
    return index, paths

# === Text Embedding Function ===
def get_text_embedding(text):
    print(f"[INFO] Creating embedding for text: \"{text}\"")
    tokens = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_embedding = model.encode_text(tokens)
        text_embedding /= text_embedding.norm(dim=-1, keepdim=True)
    return text_embedding.cpu().numpy()

# === Search Function ===
def search_images(text_query, top_k=1):
    query_embedding = get_text_embedding(text_query)
    D, I = index.search(query_embedding, top_k)
    print(f"[INFO] Retrieved top {top_k} result(s).")
    return [image_paths[i] for i in I[0]]

# === Show One Result ===
def show_result(result_path):
    print("[INFO] Displaying result...")
    img = Image.open(result_path)
    plt.figure(figsize=(6, 6))
    plt.imshow(img)
    plt.title(os.path.basename(result_path))
    plt.axis('off')
    plt.show()

# === Main Logic ===
if __name__ == "__main__":
    if os.path.exists(INDEX_FILE) and os.path.exists(PATHS_FILE):
        index, image_paths = load_index()
    else:
        images = load_images_from_folder(IMAGE_DIR)
        image_paths = [path for _, path in images]
        print("[INFO] Generating image embeddings...")
        image_inputs = torch.stack([preprocess(img).to(device) for img, _ in images])
        with torch.no_grad():
            image_embeddings = model.encode_image(image_inputs)
            image_embeddings /= image_embeddings.norm(dim=-1, keepdim=True)
        image_embeddings_np = image_embeddings.cpu().numpy()
        print("[INFO] Building FAISS index...")
        index = faiss.IndexFlatIP(image_embeddings_np.shape[1])
        index.add(image_embeddings_np)
        save_index(index, image_paths)

    # === Run Query ===
    query = input("\n🔍 Enter search text: ")
    results = search_images(query)
    print("Closest match:")
    print("  →", results[0])
    show_result(results[0])
