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
    """
    Carga el pipeline entrenado y la metadata desde el archivo joblib.

    En el notebook se guardó algo como:
    artifacts = {
        "model": pipe,
        "feature_names": X_train.columns.tolist(),
        "classes": pipe.named_steps["clf"].classes_.tolist()
    }
    joblib.dump(artifacts, "modelo_mlp_riesgo.joblib")
    """
    if not ARTIFACTS_PATH.exists():
        raise ModelNotLoadedError(f"No se encontró el archivo de modelo en: {ARTIFACTS_PATH}")

    artifacts = joblib.load(ARTIFACTS_PATH)
    model = artifacts.get("model")
    feature_names = artifacts.get("feature_names")
    classes = artifacts.get("classes")

    if model is None or feature_names is None or classes is None:
        raise ModelNotLoadedError("El archivo de modelo no contiene las claves esperadas: "
                                  "'model', 'feature_names', 'classes'.")

    return model, feature_names, classes


def build_feature_row(payload: Dict) -> Tuple[pd.DataFrame, list]:
    """
    Construye un DataFrame de una sola fila con las columnas EXACTAS
    que espera el pipeline (feature_names).

    - Si una columna no viene en el payload, se rellena con 'Desconocido'
      (categoría no vista -> OneHotEncoder la ignora).
    """
    model, feature_names, classes = load_artifacts()

    row_dict = {}

    for col in feature_names:
        # Si viene en el JSON usaremos ese valor, si no rellenamos neutro.
        value = payload.get(col, "Desconocido")
        row_dict[col] = value

    df = pd.DataFrame([row_dict], columns=feature_names)
    return df, classes


def predict_from_payload(payload: Dict) -> Tuple[str, Dict[str, float]]:
    """
    Recibe el diccionario que viene del endpoint,
    construye el DataFrame, ejecuta el modelo y devuelve:
    - clase predicha
    - probabilidades por clase
    """
    model, feature_names, classes = load_artifacts()
    X, classes_ = build_feature_row(payload)

    # Predicción
    pred = model.predict(X)[0]
    probs = model.predict_proba(X)[0]

    proba_dict: Dict[str, float] = {
        cls: float(p) for cls, p in zip(classes_, probs)
    }

    return str(pred), proba_dict
