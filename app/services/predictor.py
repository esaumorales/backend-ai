from .mlp_loader import mlp_model, mlp_feature_names, mlp_classes
import pandas as pd


def predict_from_payload(payload: dict):
    # 1. Convertir payload en DataFrame con el mismo orden y columnas
    row = pd.DataFrame([{col: payload.get(col, None) for col in mlp_feature_names}])

    # 2. Predecir
    pred = mlp_model.predict(row)[0]
    probs = mlp_model.predict_proba(row)[0]

    # 3. Convertir probabilidades a dict
    prob_dict = {cls: float(probs[i]) for i, cls in enumerate(mlp_classes)}

    return pred, float(max(probs)), prob_dict
