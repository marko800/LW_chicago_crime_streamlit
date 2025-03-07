from Dashboard import chicago_crime_sidebar, load_districts_data

import streamlit as st
import pydeck as pdk
import requests
import random

# General Settings
st.set_page_config(page_title="Chicago Crime Map Overview", page_icon="🗺️", layout="wide")

# Page content
st.title('Chicago Crime Map')

# Sidebar
chicago_crime_sidebar()

# Display Lottie animation with proper alignment
st.sidebar.header('Settings')

# Input Area
col1, col2, col3 = st.columns(3, vertical_alignment='bottom')

with col1:
    date_to_predict = st.date_input("Day to predict:", format="DD.MM.YYYY")
with col2:
    districts_geojson = load_districts_data()  # Ensure data is loaded here
    communities = sorted(
        [feature['properties']['community'] for feature in districts_geojson['features']],
        reverse=False
    )
    district_selected = st.selectbox(
        "Which district do you want to look at?",
        communities  # Already sorted
    )
with col3:
    submit = st.button("Get crime prediction", 'prediction')
    
# Map Style
map_style_options = {
    "Satellite with Streets": "mapbox://styles/mapbox/satellite-streets-v12",
    "Satellite": "mapbox://styles/mapbox/satellite-v9",
    "Dark Mode": "mapbox://styles/mapbox/dark-v11",
    "Navigation Day": "mapbox://styles/mapbox/navigation-day-v1",
    "Navigation Night": "mapbox://styles/mapbox/navigation-night-v1",
    "Street View": "mapbox://styles/mapbox/streets-v11",
    "Light v10": "mapbox://styles/mapbox/light-v10",
}
selected_style_name = st.sidebar.selectbox(
    "Select your map style:",
    list(map_style_options.keys())  # Shows keys of the dict as dropdown
)
chicago_map_style = map_style_options[selected_style_name] # Access Mapbox-Style-URL

# Data
districts_geojson = load_districts_data()

def add_prediction(districts_geojson, date_to_predict):
    def fetch_crime_predictions(date_to_predict):
        api_url = f"https://chicagocrimes-22489836433.europe-west1.run.app/predict?predict_day={date_to_predict}"
        response = requests.get(api_url)
        return response.json()['n_crimes']
    
    elevations = []
    
    # Füge den Höhenwert für jedes Feature hinzu und sammle die Höhenwerte
    for feature in districts_geojson['features']:
        #elevation = fetch_crime_predictions(date_to_predict)
        elevation = random.randint(1,100)
        feature['properties']['elevation'] = elevation
        elevations.append(elevation)

    return districts_geojson

updated_districts_geojson = add_prediction(districts_geojson, date_to_predict)


# Create the interactive map for initial load and when button is pressed
def create_map():
    return pdk.Deck(
        map_style=chicago_map_style,
        initial_view_state=pdk.ViewState(
            latitude=41.881832,
            longitude=-87.623177,
            zoom=10,
            pitch=50,
        ),
        layers=[
            # FillExtrusionLayer for 3D buildings
            pdk.Layer(
                'GeoJsonLayer',
                data=updated_districts_geojson,
                pickable=True,
                extruded=True,  # Make it extruded for all features
                elevation_scale=75,  # Adjust this scale as needed
                elevation_range=[0, 1000],  # Set the elevation range
                auto_highlight=True,
                get_fill_color=f"properties.community == '{district_selected}' ? [192, 192, 255, 250] : [192, 192, 255, 0]",
                get_elevation=f"properties.community == '{district_selected}' ? 20 : 0",  # Dynamic elevation,
            ),
            # LineLayer for borders
            pdk.Layer(
                'GeoJsonLayer',
                data=updated_districts_geojson,
                pickable=True,
                stroked=True,
                extruded=False,
                filled=True,
                auto_highlight=True,
                get_line_color=[00, 00, 80],  # Red color for borders
                get_line_width=40,  # Width of the border lines
                line_width_scale=1,
                get_fill_color=f"properties.community == '{district_selected}' ? [192, 192, 255, 0] : [192, 192, 255, 100]",
            ),
        ],
        tooltip={
            "html": "<b>District:</b> {community}<br><b>Crime Prediction:</b> {elevation}",
            "style": {"backgroundColor": "white", "color": "black"}
        }
    )

st.pydeck_chart(create_map(), use_container_width=True)