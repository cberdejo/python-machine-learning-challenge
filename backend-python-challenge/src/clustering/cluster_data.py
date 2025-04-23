import hdbscan
import polars as ps
from machine_learning.machine_learning_functions import scale_data

import hdbscan
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import numpy as np


def label_dataset_no_clustering(data: list[dict]) -> list[dict]:
    """
    Assigns labels to animals based on their characteristics.
    The labeling is done based on the following rules:

    If walks_on_n_legs == 2:
        - if has_wings == true → chicken
        - else → kangaroo
    If walks_on_n_legs == 4:
        - if weight > 150 → elephant
        - else → dog
    En cualquier otro caso → outlier


    Args:
        data (list[dict]): List of dictionaries containing animal data.

    Returns:
        list[dict]: List of dictionaries with assigned labels.
    """
    labeled_data = []

    for item in data:
        label = "outlier"

        if item.get("walks_on_n_legs") == 2:
            if item.get("has_wings"):
                label = "chicken"
            else:
                label = "kangaroo"

        elif item.get("walks_on_n_legs") == 4:
            if item.get("weight", 0) > 150:
                label = "elephant"
            else:
                label = "dog"

        # Agregamos la etiqueta al item
        item["label"] = label
        labeled_data.append(item)

    return labeled_data


def search_best_hdbscan(X):
    """
    Searches for the best HDBSCAN parameters using silhouette score.
    Args:
        X (np.ndarray): Data to be clustered.
    Returns:
        tuple: A tuple containing the best labels, parameters, and silhouette score.
    """
    best_score = -1
    best_params = {}
    best_labels = None

    for min_cluster_size in [3, 5, 10]:
        for min_samples in [1, 5, 10]:
            clusterer = hdbscan.HDBSCAN(
                min_cluster_size=min_cluster_size, min_samples=min_samples
            )
            labels = clusterer.fit_predict(X)

            # Ignora casos donde solo hay ruido
            if len(set(labels)) <= 1 or len(set(labels)) == 2 and -1 in labels:
                continue

            score = silhouette_score(X, labels)
            if score > best_score:
                best_score = score
                best_params = {
                    "min_cluster_size": min_cluster_size,
                    "min_samples": min_samples,
                }
                best_labels = labels

    return best_labels, best_params, best_score


def cluster_and_label_data(df: ps.DataFrame) -> tuple[ps.DataFrame, dict, float]:
    """
    NOT FINISHED
    Clusters the data using HDBSCAN and labels the clusters (excluding outliers).
    Args:
        df (ps.DataFrame): DataFrame with features to be clustered.
    Returns:
        tuple: Filtered labeled DataFrame, best parameters, and silhouette score.
    """
    df_scaled = scale_data(df)
    best_labels, best_params, best_score = search_best_hdbscan(df_scaled)

    # Get the best labels and add them to the DataFrame
    df = df.with_columns(ps.Series("cluster", best_labels))

    # Delete outliers (cluster -1)
    df_clean = df.filter(df["cluster"] != -1)

    n_clusters = len(set(best_labels)) - (1 if -1 in best_labels else 0)

    # Rename clusters to labels

    return df_clean, best_params, best_score
