import pandas as pd
import numpy as np
import streamlit as st

DATA_PATH = "Dataset/Data/STAR_Integrated_Data_Latest.csv"

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
def load_and_prepare_data() -> pd.DataFrame:
    '''
    Loads the original dataset and injects map coordinates dynamically using Land Bounding Boxes.
    '''
    df = pd.read_csv(DATA_PATH)
    
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
def get_working_dataframe():
    return load_and_prepare_data().copy()
