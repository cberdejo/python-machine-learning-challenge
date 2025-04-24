from typing import List
from api.models.animal_data import AnimalData
from .machine_learning_functions import (
    prepare_data_for_machine_learning,
    prepare_data_for_prediction,
    scale_data,
)
from sklearn.preprocessing import LabelEncoder
import polars as ps


def predict(
    data: List[AnimalData], model, label_encoder: LabelEncoder
) -> List[AnimalData]:
    """
    Predict the labels of the given animal data using the provided model.
    Args:
        data (List[AnimalData]): List of AnimalData objects to predict.
        model: Trained machine learning model.
        label_encoder (LabelEncoder): Label encoder for decoding labels.
    Returns:
        List[AnimalData]: List of AnimalData objects with predicted labels.
    """
    # Transform data to DataFrame
    df = ps.DataFrame(
        [
            {key: value for key, value in animal.dict().items() if key != "label"}
            for animal in data
        ]
    )

    # Prepare features for prediction
    X = prepare_data_for_prediction(df)

    # Predict using the model
    y_pred = model.predict(X)
    labels = label_encoder.inverse_transform(y_pred)

    # Add labels to the original data
    for animal, label in zip(data, labels):
        animal.label = label

    return data
