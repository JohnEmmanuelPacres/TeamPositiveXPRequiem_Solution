import pandas as pd
from sklearn.cluster import KMeans

def generate_cohorts(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Uses K-Means clustering to identify dynamic talent pools based on Age and Experience.
    '''
    work_df = df.copy()
    
    # Simple standardized feature matrix
    X = work_df[["Age", "Years_Experience"]].fillna(0)
    
    # 3 Clusters: E.g., Rookies, Mid-Levels, Veterans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
    work_df["Cohort_Cluster"] = kmeans.fit_predict(X)
    
    # Give colloquial names based on cluster centroids
    centroids = kmeans.cluster_centers_
    # Sorting by experience to assign naming
    sorted_order = centroids[:, 1].argsort()
    
    cluster_mapping = {}
    cluster_mapping[sorted_order[0]] = "Novice Pool"
    cluster_mapping[sorted_order[1]] = "Core Tier"
    cluster_mapping[sorted_order[2]] = "Veteran Legends"
    
    work_df["Cohort_Name"] = work_df["Cohort_Cluster"].map(cluster_mapping)
    return work_df
