from .machine_learning_functions import (
    evaluate_model,
    prepare_data_for_machine_learning,
    scale_data,
)
from machine_learning.models.analysis_result import AnalysisResult
import polars as ps


def validate(dataframe: ps.DataFrame, model) -> AnalysisResult:
    """
    Validate the model using the provided dataframe and model.

    Args:
        dataframe (pd.DataFrame): The input data for validation.
        model: The trained model to be validated.

    Returns:
        AnalysisResult: The result of the validation process.
    """
    X, y, _ = prepare_data_for_machine_learning(dataframe)
    X_scaled = scale_data(X)

    return evaluate_model(model, X_scaled, y)
