import math
import pandas as pd

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Approximate distance using rough hypotenuse calculation since 
    we mapped these as arbitrary grid regions for the hackathon. 
    (Haversine is more accurate but simple Euclidean suffices for quick mockups).
    """
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def find_nearest_teacher(df: pd.DataFrame, target_lat, target_lon, subject=None) -> pd.DataFrame:
    """
    Filters the dataframe for nearest available teachers optionally sorting by a specific subject.
    Returns the top candidates.
    """
    work_df = df.copy()
    if subject:
        work_df = work_df[work_df["Major_Specialization"].str.contains(subject, case=False, na=False)]
        
    distances = work_df.apply(
        lambda row: calculate_distance(target_lat, target_lon, row["Latitude"], row["Longitude"]), 
        axis=1
    )
    work_df["Distance_from_target"] = distances
    
    return work_df.sort_values(by="Distance_from_target").head(5)
