import pydeck as pdk
import pandas as pd
import streamlit as st

def create_heatmap_layer(df: pd.DataFrame) -> pdk.Layer:
    """
    Returns a hexagon density layer for the heatmap effect.
    """
    return pdk.Layer(
        "HexagonLayer",
        data=df,
        get_position=["Longitude", "Latitude"],
        auto_highlight=True,
        elevation_scale=100,
        pickable=True,
        elevation_range=[0, 3000],
        extrude=True,
        coverage=1
    )

def create_scatter_layer(df: pd.DataFrame) -> pdk.Layer:
    """
    Plots individual teachers as points.
    """
    return pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["Longitude", "Latitude"],
        get_color="[200, 30, 0, 160]",
        get_radius=200,
        pickable=True
    )

def render_map(df: pd.DataFrame, view_state=None):
    """
    Renders the pydeck map.
    """
    if view_state is None:
        view_state = pdk.ViewState(
            longitude=122.56, 
            latitude=12.2, 
            zoom=4.5, 
            min_zoom=4, 
            max_zoom=12, 
            pitch=45, 
            bearing=0
        )
    
    layers = [
        create_heatmap_layer(df),
        create_scatter_layer(df)
    ]
    
    r = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"text": "Teacher Concentration"},
        map_style="mapbox://styles/mapbox/dark-v10",
    )
    st.pydeck_chart(r)
