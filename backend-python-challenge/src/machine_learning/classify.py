import polars as ps
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .models.analysis_result import AnalysisResult
from .machine_learning_functions import (
    evaluate_model,
    prepare_data_for_machine_learning,
    train_model_with_grid_search,
)


def classify_data_using_knn(
    dataframe: ps.DataFrame,
) -> tuple[AnalysisResult, LabelEncoder]:
    """
    Function to classify data using KNN classifier.
    Args:
        dataframe (DataFrame): DataFrame containing the animal data.
    Returns:
        AnalysisResult: Object containing model results.
        LabelEncoder: Object for label encoding.
    """
    X, y, label_encoder = prepare_data_for_machine_learning(dataframe)

    grid_knn = {
        "model__n_neighbors": [3, 5, 7, 9, 11],
        "model__weights": ["uniform", "distance"],
        "model__metric": ["euclidean", "cosine", "manhattan"],
    }

    best_model, grid = train_model_with_grid_search(
        X, y, KNeighborsClassifier(), grid_knn
    )
    result = evaluate_model(best_model, X, y, label_encoder, grid_search=grid)
    return result, label_encoder


def classify_data_using_hard_voting(
    dataframe: ps.DataFrame,
) -> tuple[AnalysisResult, LabelEncoder]:
    """ "
    Function to classify data using hard voting with KNN, Decision Tree, and SVC classifiers.
    For this specific case, this is too much, but it is a good example of how to use the hard voting classifier.
    Args:
        dataframe (DataFrame): DataFrame containing the animal data.
    Returns:
        AnalysisResult: Object containing model results.
        LabelEncoder: Label encoder used for encoding the target variable.

    """

    X, y, label_encoder = prepare_data_for_machine_learning(dataframe)
    # KNN Classifier
    grid_knn = {
        "model__n_neighbors": [3, 5, 7],
        "model__weights": ["uniform", "distance"],
        "model__metric": ["euclidean", "cosine"],
    }

    knn_model, _ = train_model_with_grid_search(X, y, KNeighborsClassifier(), grid_knn)

    # Decision Tree Classifier
    grid_dtc = {
        "model__criterion": ["gini", "entropy"],
        "model__max_depth": [3, 5],
        "model__min_samples_split": [2, 4],
    }
    dtc_model, _ = train_model_with_grid_search(
        X, y, DecisionTreeClassifier(), grid_dtc
    )

    # SVC Classifier
    grid_svc = {
        "model__C": [0.1, 1],
        "model__kernel": ["linear", "rbf"],
        "model__gamma": [0.01, 0.1],
    }
    svc_model, _ = train_model_with_grid_search(X, y, SVC(), grid_svc)
    # Hard Voting Classifier
    estimators = [
        ("knn", knn_model.named_steps["model"]),
        ("dtc", dtc_model.named_steps["model"]),
        ("svc", svc_model.named_steps["model"]),
    ]
    voting_clf = VotingClassifier(estimators=estimators, voting="hard")

    result = evaluate_model(voting_clf, X, y)
    return result, label_encoder
