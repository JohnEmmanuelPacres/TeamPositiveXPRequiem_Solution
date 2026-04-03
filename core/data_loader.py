import pandas as pd
import numpy as np
import streamlit as st

import os

DATA_PATH = "Dataset/Data/STAR_Integrated_Data_Latest.csv"

def generate_historical_dataset(year: str):
    """
    Reverse-engineers realistic past datasets by degrading the current data 
    (lowering experience, increasing 'out-of-field' teaching to simulate the crisis).
    """
    base_df = pd.read_csv(DATA_PATH)
    years_back = 2026 - int(year)
    
    np.random.seed(int(year))
    # Degrade Experience and Age with random penalties to simulate non-uniform progression
    # The further back in time, the wider the variance of experience loss, padding the Novice pool
    random_xp_penalty = np.random.randint(0, 3 + (years_back * 2), size=len(base_df))
    base_df['Years_Experience'] = base_df['Years_Experience'] - years_back - random_xp_penalty
    base_df['Years_Experience'] = base_df['Years_Experience'].apply(lambda x: max(0, x))
    
    base_df['Age'] = base_df['Age'] - years_back
    base_df['Age'] = base_df['Age'].apply(lambda x: max(20, x))
    
    # Scramble specializations to simulate "out-of-field" mismatches prior to STAR program
    mismatch_percent = 0.08 * years_back # 8% worse mismatch per year back
    mismatch_count = int(len(base_df) * mismatch_percent)
    
    # Randomly assign a non-matching subject to simulate out-of-field
    indices_to_mismatch = np.random.choice(base_df.index, size=mismatch_count, replace=False)
    for i in indices_to_mismatch:
        base_df.loc[i, 'Major_Specialization'] = "Unrelated / Not Specified"
        base_df.loc[i, 'Fragility_Indicator'] = "High"

    path = f"Dataset/Data/STAR_Integrated_Data_{year}.csv"
    base_df.to_csv(path, index=False)
    return path

# Philippine strict-inland anchor coordinates (17 Regions)
REGION_COORDS = {
    "NCR": (14.65, 121.05), # Quezon City (deep inland)
    "CAR": (16.41, 120.60), # Benguet
    "Region I": (16.03, 120.44), # Pangasinan inland
    "Region II": (17.61, 121.72), # Tuguegarao
    "Region III": (15.48, 120.59), # Tarlac
    "Region IV-A": (14.16, 121.25), # Laguna inland
    "Region IV-B": (13.06, 121.13), # Oriental Mindoro inland
    "Region V": (13.62, 123.19), # Naga inland
    "Region VI": (11.00, 122.50), # Iloilo inland
    "Region VII": (10.35, 123.85), # Cebu central mountains
    "Region VIII": (11.83, 124.95), # Samar inland
    "Region IX": (8.00, 123.25), # Zamboanga del Sur inland
    "Region X": (8.15, 124.85), # Bukidnon inland
    "Region XI": (7.20, 125.40), # Davao inland
    "Region XII": (6.30, 124.80), # Cotabato
    "Region XIII": (8.60, 125.75), # Agusan
    "BARMM": (7.75, 124.30) # South of Lake Lanao
}

@st.cache_data
def load_and_prepare_data(year="2026") -> pd.DataFrame:
    '''
    Loads the original dataset and injects map coordinates dynamically using Land Bounding Boxes.
    '''
    if year == "2026":
        path = DATA_PATH
    else:
        path = f"Dataset/Data/STAR_Integrated_Data_{year}.csv"
        # Check if it was generated
        if not os.path.exists(path):
            path = generate_historical_dataset(year)
            
    df = pd.read_csv(path)
    
    # Map coordinates
    def get_lat(region):
        return REGION_COORDS.get(region, (12.8797, 121.7740))[0]

    def get_lon(region):
        return REGION_COORDS.get(region, (12.8797, 121.7740))[1]
        
    df['Latitude'] = df['Region'].apply(get_lat)
    df['Longitude'] = df['Region'].apply(get_lon)
    
    # Apply a very tight realistic jitter for Map visualization
    # Increased to 0.05 dev for realistic scattering while staying safely inland
    jitter_lat = np.random.normal(0, 0.05, size=len(df))
    jitter_lon = np.random.normal(0, 0.05, size=len(df))
    
    df['Latitude'] = df['Latitude'] + jitter_lat
    df['Longitude'] = df['Longitude'] + jitter_lon
    
    return df

# For caching the simulator modifications rapidly
@st.cache_data
def get_working_dataframe(year="2026"):
    return load_and_prepare_data(year).copy()
