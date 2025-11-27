import joblib
import pandas as pd
import os
import json

# 📌 Carpeta raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📌 Ubicación de artifacts real
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "artifacts")

# Paths correctos
kmeans_path = os.path.join(ARTIFACTS_DIR, "students_kmeans_k2.joblib")
scaler_path = os.path.join(ARTIFACTS_DIR, "students_scaler.joblib")
features_path = os.path.join(ARTIFACTS_DIR, "students_features.json")

print("KMEANS PATH:", kmeans_path)
print("SCALER PATH:", scaler_path)
print("FEATURES PATH:", features_path)

# 🔹 Cargar KMeans
kmeans = joblib.load(kmeans_path)

# 🔹 Cargar scaler (es solo el scaler)
scaler = joblib.load(scaler_path)

# 🔹 Cargar nombres de features desde JSON
with open(features_path, "r", encoding="utf-8") as f:
    feature_names = json.load(f)


def predict_cluster(payload: dict):
    """Predice el cluster usando el modelo KMeans"""

    # Crear fila en el mismo orden que feature_names
    row = [[payload.get(f) for f in feature_names]]
    df = pd.DataFrame(row, columns=feature_names)

    # Escalar
    df_scaled = scaler.transform(df)

    # Predecir cluster
    cluster = kmeans.predict(df_scaled)[0]

    return int(cluster)
