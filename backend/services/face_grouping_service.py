# backend/services/face_grouping_service.py

import os
import face_recognition
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN
from typing import List, Tuple, Dict
import json
import pickle

# Get image directory from environment variable
image_dir = os.getenv("IMAGE_DIR", "/app/images")
CLUSTER_DIR = "clusters"

# Storage files - store directly in /app directory
FACE_ENCODINGS_FILE = os.getenv("FACE_ENCODINGS_FILE", "/app/face_encodings.pkl")
FACE_CLUSTERS_FILE = os.getenv("FACE_CLUSTERS_FILE", "/app/face_clusters.json")
FACE_PATHS_FILE = os.getenv("FACE_PATHS_FILE", "/app/face_paths.txt")

def get_relative_path(absolute_path: str) -> str:
    """Convert absolute path to relative path for the frontend."""
    return absolute_path.replace("/app/images/", "")

def save_face_data(encodings: List[np.ndarray], paths: List[str], clusters: Dict):
    """Save face encodings, paths, and clusters to disk."""
    # Save encodings using pickle (numpy arrays)
    with open(FACE_ENCODINGS_FILE, 'wb') as f:
        pickle.dump(encodings, f)
    
    # Save paths
    with open(FACE_PATHS_FILE, 'w') as f:
        for path in paths:
            f.write(f"{path}\n")
    
    # Save clusters as JSON
    with open(FACE_CLUSTERS_FILE, 'w') as f:
        json.dump(clusters, f)

def load_face_data() -> Tuple[List[np.ndarray], List[str], Dict]:
    """Load face encodings, paths, and clusters from disk."""
    try:
        # Load encodings
        with open(FACE_ENCODINGS_FILE, 'rb') as f:
            encodings = pickle.load(f)
        
        # Load paths
        with open(FACE_PATHS_FILE, 'r') as f:
            paths = [line.strip() for line in f.readlines()]
        
        # Load clusters
        with open(FACE_CLUSTERS_FILE, 'r') as f:
            clusters = json.load(f)
        
        return encodings, paths, clusters
    except (FileNotFoundError, EOFError):
        return [], [], {}

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
                    paths.append(filename)
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
    
    return encodings, paths

def cluster_faces(encodings):
    clustering = DBSCAN(metric='euclidean', eps=0.6, min_samples=1)
    labels = clustering.fit_predict(encodings)
    return labels

def process_faces() -> Dict:
    """Process all faces and save the results. This is the only function that processes faces."""
    print("[INFO] Processing faces...")
    encodings, paths = load_face_encodings()
    print(f"[INFO] Found {len(encodings)} face(s)")

    if len(encodings) == 0:
        empty_result = {"clusters": {}, "total_clusters": 0}
        save_face_data([], [], empty_result["clusters"])
        return empty_result

    print("[INFO] Clustering...")
    labels = cluster_faces(encodings)

    # Create cluster map
    cluster_map = {}
    for label, path in zip(labels, paths):
        cluster_map.setdefault(str(label), []).append(path)
    
    # Save the processed data
    save_face_data(encodings, paths, cluster_map)
    print("[INFO] Saved face clusters to disk")

    return {"clusters": cluster_map, "total_clusters": len(cluster_map)}

def get_face_clusters() -> Dict:
    """Get face clusters from storage. Never reprocess - only return cached data."""
    try:
        # Try to load cached data
        encodings, paths, clusters = load_face_data()
        if encodings and paths and clusters:
            print("[INFO] Using cached face clusters")
            return {"clusters": clusters, "total_clusters": len(clusters)}
        else:
            # If no data exists, return empty result
            print("[INFO] No face clusters found in cache")
            return {"clusters": {}, "total_clusters": 0}
    except Exception as e:
        print(f"[WARN] Error loading cached face data: {e}")
        # Return empty result on error
        return {"clusters": {}, "total_clusters": 0}

def remove_deleted_face(deleted_path: str):
    """Remove a deleted image from face data and reprocess if needed."""
    try:
        encodings, paths, clusters = load_face_data()
        if not paths:
            return

        # Convert the deleted path to relative path
        relative_path = os.path.basename(deleted_path)
        
        # Check if this image had any faces
        if relative_path in paths:
            # Reprocess all faces since we can't easily remove individual faces
            process_faces()
            print(f"[Face] Reprocessed faces after removing: {relative_path}")
    except Exception as e:
        print(f"[Face] Error removing deleted face: {e}")
        # If there's an error, reprocess everything
        process_faces()
