import pandas as pd
from sklearn.cluster import KMeans
from core.dataframe_schema import normalize_record_columns

def generate_cohorts(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Uses K-Means clustering to identify dynamic talent pools based on Age and Experience.
    '''
    work_df = normalize_record_columns(df, include_legacy_aliases=True)
    
    # Simple standardized feature matrix
    X = work_df[["age", "years_experience"]].fillna(0)
    
    # 3 Clusters: E.g., Rookies, Mid-Levels, Veterans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
    work_df["cohort_cluster"] = kmeans.fit_predict(X)
    
    # Give colloquial names based on cluster centroids
    centroids = kmeans.cluster_centers_
    # Sorting by experience to assign naming
    sorted_order = centroids[:, 1].argsort()
    
    cluster_mapping = {}
    cluster_mapping[sorted_order[0]] = "Novice Pool"
    cluster_mapping[sorted_order[1]] = "Core Tier"
    cluster_mapping[sorted_order[2]] = "Veteran Legends"
    
    work_df["cohort_name"] = work_df["cohort_cluster"].map(cluster_mapping)
    return normalize_record_columns(work_df, include_legacy_aliases=True)
