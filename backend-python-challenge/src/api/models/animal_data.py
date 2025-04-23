from api.models.synthetic_data import SyntheticDataParams
from pydantic import BaseModel
from typing import Any, List, Optional


class AnimalData(BaseModel):
    walks_on_n_legs: int
    height: float
    weight: float
    has_wings: bool
    has_tail: bool
    label: Optional[str] = None  # Optional label for the animal data


class PredictRequest(BaseModel):
    model: SyntheticDataParams
    data: List[AnimalData]
