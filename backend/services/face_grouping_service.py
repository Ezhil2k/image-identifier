# backend/services/face_grouping_service.py

import os
import face_recognition
import numpy as np
from sklearn.cluster import DBSCAN

IMAGE_DIR = "images"
CLUSTER_DIR = "clusters"

def load_face_encodings(image_dir=IMAGE_DIR):
    encodings = []
    paths = []

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(image_dir, filename)
            img = face_recognition.load_image_file(path)
            face_bounding_boxes = face_recognition.face_locations(img)

            if face_bounding_boxes:
                face_encoding = face_recognition.face_encodings(
                    img, known_face_locations=face_bounding_boxes
                )[0]
                encodings.append(face_encoding)
                paths.append(path)

    return np.array(encodings), paths

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
