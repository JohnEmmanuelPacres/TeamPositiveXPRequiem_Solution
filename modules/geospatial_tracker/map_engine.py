import pydeck as pdk
import pandas as pd
import streamlit as st

def create_heatmap_layer(df: pd.DataFrame) -> pdk.Layer:
    """
    Returns a hexagon density layer for the heatmap effect.
    """
    # Adding a vibrant color palette to make it look professional and appealing
    COLOR_RANGE = [
        [255, 255, 178],
        [254, 204, 92],
        [253, 141, 60],
        [240, 59, 32],
        [189, 0, 38],
    ]

    return pdk.Layer(
        "HexagonLayer",
        data=df,
        get_position=["Longitude", "Latitude"],
        auto_highlight=True,
        radius=5000, # Massive 5km cell radius makes the data bloom comprehensively across the map
        elevation_scale=300, # Boosted elevation so the wider hexagons still shoot up
        pickable=True,
        elevation_range=[0, 3000],
        extrude=True,
        coverage=1,
        color_range=COLOR_RANGE,
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
        # Changed max_zoom to 20 so users can zoom in close enough to see 3D buildings.
        view_state = pdk.ViewState(
            longitude=122.56, 
            latitude=12.2, 
            zoom=4.5, 
            min_zoom=4, 
            max_zoom=20, 
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
        # Switch to "carto" so it works automatically without any API keys! 
        map_provider="carto", 
        # "voyager" style is Carto's equivalent to Google Maps (roads, labels, light background)
        map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
    )
    st.pydeck_chart(r)
