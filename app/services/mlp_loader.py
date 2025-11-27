import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "modelo_mlp_riesgo.joblib")

mlp_artifacts = joblib.load(MODEL_PATH)

mlp_model = mlp_artifacts["model"]
mlp_feature_names = mlp_artifacts["feature_names"]
mlp_classes = mlp_artifacts["classes"]
