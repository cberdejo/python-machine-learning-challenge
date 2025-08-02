from sklearn.cluster import KMeans
import polars as pl


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


def label_dataset_with_clustering_polars(data: list[dict]) -> list[dict]:
    """
    Labels a dataset of animals using clustering and domain-specific rules with Polars.

    Clusters the data into 4 groups using KMeans and assigns labels based on:
    - Number of legs
    - Presence of wings
    - Average weight of the cluster

    Returns:
        list[dict]: Original data with an added 'label' field.
    """
    df = pl.DataFrame(data)

    # Convert boolean to int
    df = df.with_columns(
        [pl.col("has_tail").cast(pl.Int8), pl.col("has_wings").cast(pl.Int8)]
    )

    # Extract features for clustering
    features_df = df.select(
        ["walks_on_n_legs", "height", "weight", "has_tail", "has_wings"]
    )
    features = features_df.to_numpy()

    # Apply KMeans
    kmeans = KMeans(n_clusters=4, random_state=42, n_init="auto")
    clusters = kmeans.fit_predict(features)

    # Add cluster info
    df = df.with_columns(pl.Series(name="cluster", values=clusters))

    # Compute average metrics by cluster
    cluster_groups = df.groupby("cluster").agg(
        [
            pl.col("walks_on_n_legs").mode().alias("mode_legs"),
            pl.col("has_wings").mean().alias("mean_wings"),
            pl.col("weight").mean().alias("mean_weight"),
        ]
    )

    # Determine labels per cluster
    label_map = {}
    weight_mean_global = df.select(pl.col("weight").mean()).item()

    for row in cluster_groups.iter_rows(named=True):
        if row["mode_legs"] == 2:
            label_map[row["cluster"]] = (
                "chicken" if row["mean_wings"] > 0.5 else "kangaroo"
            )
        elif row["mode_legs"] == 4:
            label_map[row["cluster"]] = (
                "elephant" if row["mean_weight"] > weight_mean_global else "dog"
            )
        else:
            label_map[row["cluster"]] = "outlier"

    # Apply labels
    df = df.with_columns(pl.col("cluster").map_dict(label_map).alias("label"))

    return df.drop("cluster").to_dicts()
