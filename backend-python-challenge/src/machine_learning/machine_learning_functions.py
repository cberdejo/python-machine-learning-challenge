import polars as ps
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import logging
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.pipeline import Pipeline


from machine_learning.models.analysis_result import AnalysisResult


logger = logging.getLogger(__name__)


def prepare_data_for_prediction(df: ps.DataFrame) -> np.ndarray:
    """
    Prepares the DataFrame for prediction by applying the same transformations
    as during training, except label encoding.
    Args:
        df (ps.DataFrame): DataFrame containing the animal data.
    Returns:
        np.ndarray: Features array for prediction.
    """
    df = df.with_columns([df["has_wings"].cast(int), df["has_tail"].cast(int)])

    feature_cols = ["height", "weight", "walks_on_n_legs", "has_wings", "has_tail"]
    X = df.select(feature_cols).to_numpy()

    return X


def prepare_data_for_machine_learning(
    df: ps.DataFrame,
) -> tuple[np.ndarray, np.ndarray, LabelEncoder]:
    """
    Prepares the DataFrame for machine learning by encoding and cleaning data.
    Args:
        df (ps.DataFrame): DataFrame containing the animal data.
    Returns:
        tuple: Tuple containing the features (X) and target variable (y) and the label encoder.
    """
    # Convertir booleanos a int
    df = df.with_columns([df["has_wings"].cast(int), df["has_tail"].cast(int)])

    # Eliminar outliers
    df = df.filter(df["label"] != "outlier")

    # Codificar la columna target
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df["label"].to_numpy())

    # Selección de características
    feature_cols = ["height", "weight", "walks_on_n_legs", "has_wings", "has_tail"]
    X = df.select(feature_cols).to_numpy()

    return X, y, label_encoder


def scale_data(X: np.ndarray) -> np.ndarray:
    """
    Scales the features using StandardScaler.
    Args:
        X (np.ndarray): Features array.
    Returns:
        np.ndarray: Scaled features array.
    """
    scaler = StandardScaler()
    return scaler.fit_transform(X)


def split_data(X, y, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    Splits the dataset into training and testing sets.
    Args:
        X (pd.DataFrame): Features DataFrame.
        y (pd.Series): Target variable Series.
        test_size (float): Proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.
    Returns:
            tuple: X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test


def train_model_with_grid_search(
    X: np.ndarray,
    y: np.ndarray,
    model,
    param_grid: dict,
    scoring: str = "accuracy",
    cv: int = 5,
    verbose: bool = False,
) -> tuple:
    """Entrena modelo usando GridSearchCV con pipeline de escalado."""

    grid = GridSearchCV(model, param_grid, scoring=scoring, cv=cv, n_jobs=-1)
    grid.fit(X, y)

    if verbose:
        logger.info(f"Best hyperparams: {grid.best_params_}")
        logger.info(f"Best validation score: {grid.best_score_:.4f}")

    return grid.best_estimator_, grid


def evaluate_model(
    model,
    X: np.ndarray,
    y: np.ndarray,
    grid_search: GridSearchCV | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
    verbose: bool = False,
) -> AnalysisResult:
    """Evalúa el modelo y devuelve un objeto AnalysisResult."""

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted")
    rec = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")
    cm = confusion_matrix(y_test, y_pred)

    if verbose:
        logger.info(
            f"Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}"
        )

    best_params = grid_search.best_params_ if grid_search else None
    best_score = grid_search.best_score_ if grid_search else None

    return AnalysisResult(
        model=model,
        best_params=best_params,
        best_score=best_score,
        accuracy=acc,
        precision=prec,
        recall=rec,
        f1=f1,
        confusion_matrix=cm.tolist(),
    )
