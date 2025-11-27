from .mlp_loader import mlp_model, mlp_feature_names, mlp_classes
import pandas as pd
from app.utils.normalizer import normalize


def predict_from_payload(payload: dict):

    # 1. Normalizar categorías antes de armar el DataFrame
    clean = normalize(payload)

    # 2. Convertir payload normalizado en DataFrame
    row = pd.DataFrame([{col: clean.get(col, None) for col in mlp_feature_names}])

    # 3. Predecir
    pred = mlp_model.predict(row)[0]
    probs = mlp_model.predict_proba(row)[0]

    # 4. Probabilidades como dict
    prob_dict = {cls: float(probs[i]) for i, cls in enumerate(mlp_classes)}

    return pred, float(max(probs)), prob_dict
