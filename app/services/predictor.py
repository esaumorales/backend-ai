from pathlib import Path
from functools import lru_cache
from typing import Dict, Tuple

import joblib
import pandas as pd

ARTIFACTS_PATH = Path(__file__).resolve().parent.parent / "artifacts" / "modelo_mlp_riesgo.joblib"


class ModelNotLoadedError(RuntimeError):
    pass


@lru_cache
def load_artifacts():
    if not ARTIFACTS_PATH.exists():
        raise ModelNotLoadedError(f"No se encontró el archivo del modelo: {ARTIFACTS_PATH}")

    artifacts = joblib.load(ARTIFACTS_PATH)
    model = artifacts.get("model")
    feature_names = artifacts.get("feature_names")
    classes = artifacts.get("classes")

    return model, feature_names, classes


def build_feature_row(payload: Dict):
    model, feature_names, _ = load_artifacts()

    row = {col: payload.get(col, "Desconocido") for col in feature_names}
    df = pd.DataFrame([row], columns=feature_names)
    return df


def predict_from_payload(payload: Dict) -> Tuple[str, float, Dict[str, float]]:
    model, feature_names, classes = load_artifacts()

    X = build_feature_row(payload)

    label = model.predict(X)[0]
    probas = model.predict_proba(X)[0]

    proba_dict = {cls: float(p) for cls, p in zip(classes, probas)}

    score = max(probas)  # ← rendimiento real

    return label, score, proba_dict
