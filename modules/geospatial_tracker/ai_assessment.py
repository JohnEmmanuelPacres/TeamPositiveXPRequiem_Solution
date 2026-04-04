import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def find_vulnerability_epicenter(df: pd.DataFrame, region: str):
    # 1. Filter for the specific region
    region_df = df[df["region"] == region].copy()
    
    # 2. Identify vulnerable teachers (Values normalized)
    vulnerable_df = region_df[
        region_df["subject_taught"].str.strip().str.lower() != 
        region_df["major_specialization"].str.strip().str.lower()
    ].copy()
    
    if len(vulnerable_df) < 3: # Lowered threshold to 3 for demo purposes
        return None, None
        
    # 3. Handle coordinate column casing
    lat_col = 'latitude' if 'latitude' in vulnerable_df.columns else 'Latitude'
    lon_col = 'longitude' if 'longitude' in vulnerable_df.columns else 'Longitude'
    
    coords = vulnerable_df[[lat_col, lon_col]].dropna()
    if coords.empty:
        return None, None

    # 4. K-Means clustering
    n_clusters = min(3, len(coords))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    
    # Predict clusters
    vulnerable_df.loc[coords.index, 'Cluster'] = kmeans.fit_predict(coords)
    
    # 5. Find the largest cluster
    cluster_counts = vulnerable_df['Cluster'].value_counts()
    if cluster_counts.empty:
        return None, None
        
    largest_cluster_id = int(cluster_counts.idxmax()) # Fixed integer cast
    epicenter_lat, epicenter_lon = kmeans.cluster_centers_[largest_cluster_id]
    
    epicenter_df = vulnerable_df[vulnerable_df['Cluster'] == largest_cluster_id]
    return (epicenter_lat, epicenter_lon), epicenter_df

def generate_ai_assessment(epicenter_df: pd.DataFrame, region: str) -> str:
    if epicenter_df is None or len(epicenter_df) == 0:
        return f"Structural Integrity High: No significant vulnerability clusters found in {region}."
        
    avg_exp = pd.to_numeric(epicenter_df['years_experience'], errors='coerce').mean()
    subject_modes = epicenter_df['subject_taught'].mode()
    most_needed_subject = subject_modes[0] if not subject_modes.empty else "Core STEM"
    
    total_teachers = len(epicenter_df)
    
    return (
        f"**Autonomous Assessment for {region}:** Isolated a cluster of **{total_teachers}** "
        f"teachers working out-of-field. The primary pedagogical gap is in **{most_needed_subject}**. "
        f"Average tenure in this hotspot is **{avg_exp:.1f} years**. "
        "Recommendation: Target this epicenter for localized subject-matter re-certification."
    )