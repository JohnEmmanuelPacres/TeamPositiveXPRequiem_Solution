import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def find_vulnerability_epicenter(df: pd.DataFrame, region: str):
    """
    Finds the largest cluster of highly vulnerable (out-of-field) teachers 
    in a specific region.
    """
    region_df = df[df["Region"] == region]
    
    # Define vulnerability (Out-of-field teaching)
    vulnerable_df = region_df[region_df["Subject_Taught"] != region_df["Major_Specialization"]].copy()
    
    # If not enough vulnerable teachers, just fall back
    if len(vulnerable_df) < 5:
        return None, None
        
    coords = vulnerable_df[['Latitude', 'Longitude']]
    
    # K-Means clustering to find 3 localized hotspots
    n_clusters = min(3, len(vulnerable_df))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    vulnerable_df['Cluster'] = kmeans.fit_predict(coords)
    
    # Find the cluster with the highest density (most teachers)
    cluster_counts = vulnerable_df['Cluster'].value_counts()
    largest_cluster_id = cluster_counts.idxmax()
    
    # Get the epicenter coordinates for the largest cluster
    epicenter_lat, epicenter_lon = kmeans.cluster_centers_[largest_cluster_id]
    
    # Extract structural data about this specific cluster to inform the assessment
    epicenter_df = vulnerable_df[vulnerable_df['Cluster'] == largest_cluster_id]
    
    return (epicenter_lat, epicenter_lon), epicenter_df

def generate_ai_assessment(epicenter_df: pd.DataFrame, region: str) -> str:
    """
    Simulates a generative AI reading the structural data of the hotspot and outputting an assessment.
    """
    if epicenter_df is None or len(epicenter_df) == 0:
        return f"Insufficient vulnerability data to generate a micro-targeted STAR assessment for {region}."
        
    avg_exp = epicenter_df['Years_Experience'].mean()
    most_needed_subject = epicenter_df['Subject_Taught'].mode()[0]
    total_teachers = len(epicenter_df)
    
    assessment = (
        f"**Micro-Targeting Assessment Complete.**\n\n"
        f"I have analyzed the geospatial distribution of vulnerable teachers in **{region}**. "
        f"The algorithm isolated an epicenter where **{total_teachers}** educators are structurally out-of-field. "
        f"The primary pedagogical deficit here is **{most_needed_subject}**.\n\n"
        f"Furthermore, with an average teaching experience of just **{avg_exp:.1f} years** inside this sub-cluster, "
        f"these teachers critically lack access to senior mentorship while handling subjects they did not major in. "
        f"**Recommendation:** Deploy immediate STAR capacity-building modules focusing on core {most_needed_subject} fundamentals directed to these specific coordinates to prevent imminent educator burnout."
    )
    
    return assessment
