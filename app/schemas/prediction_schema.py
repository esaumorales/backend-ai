from pydantic import BaseModel
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_class: str
    probabilities: Dict[str, float]
