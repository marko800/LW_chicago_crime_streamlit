import streamlit as st
import requests
from streamlit_lottie import st_lottie
import geopandas as gpd
from shapely.geometry import shape
import json

def meine_funktion():
    print("Das ist eine Funktion aus Dashboard.py")

# Configuration of the site
def chicago_crime_header():
    st.set_page_config(page_title="Chicago Crime Prediction", page_icon="👮‍♂️", layout="wide")
    
chicago_crime_header()

# Sidebar
def chicago_crime_sidebar():
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    
    with st.sidebar:
        container = st.container()  # Container für die Lottie-Animation
        with container:
            lottie_hello = load_lottieurl("https://lottie.host/ddc9bd14-5703-49fa-884c-c9236a48405f/y32PAxRVIG.json")
            st_lottie(lottie_hello, key="hello", height=150, width=100)
        
    st.sidebar.header("Menü")
    st.sidebar.page_link("Dashboard.py", label="Overview", icon="🚔")
    st.sidebar.page_link("pages/Statistics.py", label="Statistics", icon="💯")
    st.sidebar.page_link("pages/Map.py", label="Map", icon="🗺️")
    st.sidebar.page_link("pages/Heatmap.py", label="Heatmap", icon="📊")
    st.sidebar.page_link("pages/Prediction.py", label="Prediction", icon="📈")

chicago_crime_sidebar()

# General district data
@st.cache_data
def load_districts_data():
    # Pfad zur lokalen JSON-Datei
    file_path = 'data/geodata.json'
    
    # Daten aus der lokalen Datei lesen
    with open(file_path, 'r', encoding='utf-8') as file:
        districts_json = json.load(file)
    
    # Capitalize the community names in the JSON data
    for district in districts_json:
        if 'community' in district:
            district['community'] = district['community'].title()
    
    # Create GeoDataFrame
    districts = gpd.GeoDataFrame.from_features([{
        'geometry': shape(district['the_geom']),
        'properties': district
    } for district in districts_json])
    
    # Change GeoDataFrame in GeoJSON-Format
    districts_geojson = json.loads(districts.to_json())
    return districts_geojson

# Page content
st.title("Welcome to Chicago's Crime Analytics")
st.warning("ITS A WORK ON PROCESS.")
st.markdown("""Predicting crime trends is inherently challenging, even when leveraging robust statistical models grounded in historical data. Some factors that influence crime, such as the day of the week, weather patterns, and holidays, can be anticipated with relative precision. However, many others remain unpredictable. Few, if any, foresaw the COVID-19 pandemic, the nationwide protests following George Floyd’s murder, or the recent surge in inflation, events that have had profound impacts on societal behavior and, consequently, on crime rates.
            
In our analysis, we explored various time units to predict crime trends, examining the number of crimes per day, week, month, quarter, and even year. We applied different models, including ARIMA and SARIMA, to identify the most significant patterns. Ultimately, the most meaningful results were found in daily crime data, which became the focus of our analysis.

Despite our efforts to use variables such as weather conditions, holidays, and weekdays, these factors did not significantly alter our predictions. This led us to refocus on the number of crimes and community areas, where more consistent patterns emerged.

Nonetheless, it is crucial to acknowledge that unexpected events, like another public health crisis, episodes of civil unrest, or shifts in economic stability, can dramatically reshape the landscape of crime. While some effects, like those of the COVID-19 pandemic, may seem temporary, they could have long-lasting repercussions, such as changes in urban mobility or persistent educational deficits from school closures.

The key takeaway is the need for caution and flexibility in crime forecasting. Models must be continuously updated to reflect new data and the evolving conditions of each community. This approach helps mitigate the inherent uncertainty in predicting crime, ensuring that policies are responsive to both predictable trends and unforeseen challenges.
""")

st_lottie("https://lottie.host/90eb7346-7c52-4a86-bb9c-6cd5b5d93800/3ciMAFX8GE.json",
          key="arrest", height=350, width=350)