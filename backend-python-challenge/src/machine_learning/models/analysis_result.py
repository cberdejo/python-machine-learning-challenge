from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List


class AnalysisResult(BaseModel):
    best_params: Optional[Dict[str, Any]] = Field(
        None, description="Best hyperparameters found during search"
    )
    best_score: Optional[float] = Field(None, description="Best cross-validation score")
    accuracy: Optional[float] = Field(None, description="Accuracy on test set")
    precision: Optional[float] = Field(None, description="Precision on test set")
    recall: Optional[float] = Field(None, description="Recall on test set")
    f1: Optional[float] = Field(None, description="F1 score on test set")
    confusion_matrix: Optional[List[List[int]]] = Field(
        None, description="Confusion matrix as a nested list"
    )

    model: Optional[Any] = Field(None, exclude=True)  # not to be serialized
