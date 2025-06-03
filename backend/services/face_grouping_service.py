# backend/services/face_grouping_service.py

import os
import face_recognition
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Tuple, Dict

# Get image directory from environment variable
image_dir = os.getenv("IMAGE_DIR", "/app/images")
CLUSTER_DIR = "clusters"

def get_relative_path(absolute_path: str) -> str:
    """Convert absolute path to relative path for the frontend."""
    # Remove the /app prefix and any leading slashes
    relative_path = absolute_path.replace("/app/images/", "")
    return relative_path

def load_face_encodings() -> Tuple[List[np.ndarray], List[str]]:
    """Load face encodings from all images in the directory."""
    encodings = []
    paths = []
    
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, filename)
            try:
                # Load image and find face encodings
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                
                # Add each face encoding and its corresponding image path
                for encoding in face_encodings:
                    encodings.append(encoding)
                    # Store relative path for frontend
                    paths.append(filename)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
    
    return encodings, paths

def cluster_faces(encodings):
    clustering = DBSCAN(metric='euclidean', eps=0.6, min_samples=1)
    labels = clustering.fit_predict(encodings)
    return labels

def group_faces():
    print("[INFO] Encoding faces...")
    encodings, paths = load_face_encodings()
    print(f"[INFO] Found {len(encodings)} face(s)")

    if len(encodings) == 0:
        return {"clusters": {}, "message": "No faces found."}

    print("[INFO] Clustering...")
    labels = cluster_faces(encodings)

    cluster_map = {}
    for label, path in zip(labels, paths):
        cluster_map.setdefault(str(label), []).append(path)

    return {"clusters": cluster_map, "total_clusters": len(cluster_map)}
