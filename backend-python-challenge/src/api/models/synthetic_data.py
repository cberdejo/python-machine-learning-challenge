from pydantic import BaseModel
from typing import Any, List, Optional


class SyntheticDataParams(BaseModel):
    seed: int
    number_of_datapoints: int


class ValidateRequest(BaseModel):
    model: SyntheticDataParams
    data: SyntheticDataParams
