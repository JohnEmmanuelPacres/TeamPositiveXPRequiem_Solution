import math
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from core.dataframe_schema import normalize_record_columns

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Approximate distance using rough hypotenuse calculation since 
    we mapped these as arbitrary grid regions for the hackathon. 
    (Haversine is more accurate but simple Euclidean suffices for quick mockups).
    """
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

@st.cache_data
def find_nearest_teacher(df: pd.DataFrame, target_lat, target_lon, subject=None, source_region=None) -> pd.DataFrame:
    """
    Filters the dataframe for nearest available highly-qualified mentors.
    It intentionally excludes vulnerable teachers to ensure we are deploying resources cleanly.
    """
    df = normalize_record_columns(df, include_legacy_aliases=True)
    # Only deploy robust teachers who are actually teaching their correct majors
    work_df = df[df['fragility_indicator'] == 'Low'].copy()
    
    if source_region and source_region != "Global Nearest (Any)":
        work_df = work_df[work_df["region"] == source_region]
    
    if subject:
        work_df = work_df[work_df["major_specialization"].str.contains(subject, case=False, na=False)]
        
    distances = work_df.apply(
        lambda row: calculate_distance(target_lat, target_lon, row["latitude"], row["longitude"]),
        axis=1
    )
    work_df["distance_from_target"] = distances
    
    # Prevent deploying teachers who are already inside the hyper-localized epicenter hotspot
    work_df = work_df[work_df["distance_from_target"] > 0.05]
    
    return work_df.sort_values(by="distance_from_target").head(5)

@st.cache_data
def find_teachers_from_top_clusters(df: pd.DataFrame, region: str, target_lat: float, target_lon: float, subject=None, n_clusters=5, top_n_clusters=3, teachers_per_cluster=2) -> pd.DataFrame:
    """
    Clusters highly-qualified teachers in a region to find the top populated areas,
    and deploys the best/closest teachers from those areas to the target epicenter.
    """
    df = normalize_record_columns(df, include_legacy_aliases=True)
    region_df = df[df["region"] == region]
    # Only deploy robust teachers who are actually teaching their correct majors
    work_df = region_df[region_df['fragility_indicator'] == 'Low'].copy()
    
    if subject:
        work_df = work_df[work_df["major_specialization"].str.contains(subject, case=False, na=False)]
        
    distances = work_df.apply(
        lambda row: calculate_distance(target_lat, target_lon, row["latitude"], row["longitude"]),
        axis=1
    )
    work_df["distance_from_target"] = distances
    
    # Prevent deploying teachers who are already inside the hyper-localized epicenter hotspot
    work_df = work_df[work_df["distance_from_target"] > 0.05]
    
    if len(work_df) < top_n_clusters:
        return work_df.sort_values(by="distance_from_target").head(5)
        
    actual_clusters = min(n_clusters, len(work_df) // 2)
    actual_clusters = max(1, actual_clusters)
    
    coords = work_df[['latitude', 'longitude']].values
    kmeans = KMeans(n_clusters=actual_clusters, random_state=42, n_init='auto')
    work_df['cluster'] = kmeans.fit_predict(coords)
    
    cluster_counts = work_df['cluster'].value_counts()
    top_clusters = cluster_counts.nlargest(top_n_clusters).index.tolist()
    
    selected_teachers = []
    for cluster_id in top_clusters:
        cluster_df = work_df[work_df['cluster'] == cluster_id]
        # Select the closest or best matching teachers from this specific cluster
        selected = cluster_df.sort_values(by="distance_from_target").head(teachers_per_cluster)
        selected_teachers.append(selected)
        
    if not selected_teachers:
        return pd.DataFrame()
        
    result_df = pd.concat(selected_teachers, ignore_index=True)
    return result_df.sort_values(by="distance_from_target")

