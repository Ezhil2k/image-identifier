#face_grouping.py

import os
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN
from PIL import Image
import matplotlib.pyplot as plt

IMAGE_DIR = "../images"
CLUSTER_DIR = "clusters"

def load_face_encodings(image_dir):
    encodings = []
    paths = []

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(image_dir, filename)
            img = face_recognition.load_image_file(path)
            face_bounding_boxes = face_recognition.face_locations(img)

            if face_bounding_boxes:
                face_encoding = face_recognition.face_encodings(img, known_face_locations=face_bounding_boxes)[0]
                encodings.append(face_encoding)
                paths.append(path)

    return np.array(encodings), paths

def cluster_faces(encodings):
    clustering = DBSCAN(metric='euclidean', eps=0.6, min_samples=1)
    labels = clustering.fit_predict(encodings)
    return labels

def save_clusters(labels, paths):
    os.makedirs(CLUSTER_DIR, exist_ok=True)
    cluster_map = {}

    for label, path in zip(labels, paths):
        cluster_map.setdefault(label, []).append(path)

    for cluster_id, image_paths in cluster_map.items():
        print(f"[Cluster {cluster_id}] {len(image_paths)} image(s)")
        for p in image_paths:
            print("  →", os.path.basename(p))

if __name__ == "__main__":
    print("[INFO] Encoding faces...")
    encodings, paths = load_face_encodings(IMAGE_DIR)
    print(f"[INFO] Found {len(encodings)} face(s)")

    print("[INFO] Clustering...")
    labels = cluster_faces(encodings)

    save_clusters(labels, paths)
