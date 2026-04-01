import pandas as pd
import numpy as np
import streamlit as st

DATA_PATH = "Dataset/Data/STAR_Integrated_Data_20260401_2324.csv"

# Philippine approximate regional coordinates (17 Regions)
REGION_COORDS = {
    "NCR": (14.5995, 120.9842),
    "CAR": (17.0658, 121.0560),
    "Region I": (16.6159, 120.3186),
    "Region II": (17.5878, 121.7336),
    "Region III": (15.4828, 120.7120),
    "Region IV-A": (14.1008, 121.0794),
    "Region IV-B": (11.2359, 119.3499),
    "Region V": (13.4210, 123.4137),
    "Region VI": (10.9997, 122.5489),
    "Region VII": (10.3157, 123.8854),
    "Region VIII": (11.2430, 125.0081),
    "Region IX": (8.1633, 123.0069),
    "Region X": (8.1691, 124.8465),
    "Region XI": (7.2227, 125.7533),
    "Region XII": (6.1360, 124.8465),
    "Region XIII": (8.8402, 125.9262),
    "BARMM": (7.2023, 124.2422)
}

@st.cache_data
def load_and_prepare_data() -> pd.DataFrame:
    '''
    Loads the original dataset and injects map coordinates dynamically.
    '''
    df = pd.read_csv(DATA_PATH)
    
    # Map coordinates
    def get_lat(region):
        return REGION_COORDS.get(region, (12.8797, 121.7740))[0] # default center

    def get_lon(region):
        return REGION_COORDS.get(region, (12.8797, 121.7740))[1] # default center
        
    df['Latitude'] = df['Region'].apply(get_lat)
    df['Longitude'] = df['Region'].apply(get_lon)
    
    # Apply a realistic jitter for Map visualization
    # Ensures nodes aren't stacked identically on PyDeck
    jitter_lat = np.random.normal(0, 0.4, size=len(df))
    jitter_lon = np.random.normal(0, 0.4, size=len(df))
    
    df['Latitude'] = df['Latitude'] + jitter_lat
    df['Longitude'] = df['Longitude'] + jitter_lon
    
    return df

# For caching the simulator modifications rapidly
@st.cache_data
def get_working_dataframe():
    return load_and_prepare_data().copy()
