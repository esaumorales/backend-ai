# app/services/predictor.py

from pathlib import Path
from functools import lru_cache
from typing import Dict, Tuple

import joblib
import pandas as pd

# Ruta al modelo MLP guardado (pipeline completo)
ARTIFACTS_PATH = (
    Path(__file__).resolve().parent.parent / "artifacts" / "modelo_mlp_riesgo.joblib"
)


class ModelNotLoadedError(RuntimeError):
    pass


# ============================================================
# 🔹 Cargar artefactos: pipeline + nombres de columnas + clases
# ============================================================
@lru_cache
def load_artifacts():
    if not ARTIFACTS_PATH.exists():
        raise ModelNotLoadedError(
            f"No se encontró el archivo del modelo: {ARTIFACTS_PATH}"
        )

    artifacts = joblib.load(ARTIFACTS_PATH)

    if not isinstance(artifacts, dict):
        raise ModelNotLoadedError(
            "El archivo joblib no contiene un diccionario de artefactos."
        )

    model = artifacts.get("model")  # <- ES EL PIPELINE COMPLETO
    feature_names = artifacts.get("feature_names")
    classes = artifacts.get("classes")

    if model is None or feature_names is None:
        raise ModelNotLoadedError(
            "Los artefactos no contienen 'model' o 'feature_names'."
        )

    # Si por algún motivo no vinieran las clases, las sacamos del clf
    if classes is None and hasattr(model, "named_steps"):
        clf = model.named_steps.get("clf")
        if clf is not None and hasattr(clf, "classes_"):
            classes = list(clf.classes_)

    return model, feature_names, classes


# ============================================================
# 🔹 Construir DataFrame con los mismos campos que el training
# ============================================================
def build_feature_dataframe(payload: Dict) -> pd.DataFrame:
    """
    Crea un DataFrame con las MISMAS columnas y nombres que se usaron
    para entrenar el pipeline (todas categóricas).

    No convertimos a float ni tocamos los valores: dejamos las cadenas
    tal cual, porque el ColumnTransformer + OneHotEncoder se encargan.
    """
    _, feature_names, _ = load_artifacts()

    row = {}
    for col in feature_names:
        # Si falta una clave en el payload, ponemos un valor dummy
        # que el OneHotEncoder ignorará (handle_unknown="ignore")
        row[col] = payload.get(col, "Desconocido")

    df = pd.DataFrame([row], columns=feature_names)
    return df


# ============================================================
# 🔹 Predicción desde el payload del estudiante
# ============================================================
def predict_from_payload(payload: Dict) -> Tuple[str, float, Dict[str, float]]:
    """
    Recibe el payload (diccionario) que devuelve Student.to_payload()
    y retorna:

    - predicted_class: etiqueta ('Excelente', 'Satisfactorio', 'Insuficiente')
    - score: probabilidad máxima (float)
    - probabilities: dict {clase: probabilidad}
    """
    model, feature_names, classes = load_artifacts()

    df = build_feature_dataframe(payload)  # DataFrame con columnas categóricas

    # El pipeline ya hace: OneHotEncoder -> StandardScaler -> MLP
    y_pred = model.predict(df)[0]
    probas = model.predict_proba(df)[0]

    if classes is None:
        # fallback por si acaso
        if hasattr(model, "named_steps") and "clf" in model.named_steps:
            classes = list(model.named_steps["clf"].classes_)
        else:
            classes = []

    proba_dict = {cls: float(p) for cls, p in zip(classes, probas)}
    score = float(max(probas))

    return y_pred, score, proba_dict
