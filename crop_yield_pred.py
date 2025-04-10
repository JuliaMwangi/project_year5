import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import joblib

st.set_page_config(page_title="Maize Yield Prediction", layout="wide")

st.title("Maize Yield Prediction Map")

# Load model
@st.cache_resource
def load_model():
    with open("rf.joblib", "rb") as f:
        return joblib.load(f)

model = load_model()

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("D:/ACADEMICS/5TH YEAR/PROJECT/OUTPUTS/crop_yield.csv")
    return df

df = load_data()


# Sidebar for filtering or selecting year
years = df["YEAR"].unique()
selected_year = st.sidebar.selectbox("Select Year", sorted(years))

# Filter data
filtered = df[df["YEAR"] == selected_year]
filtered["Quantity"] = pd.to_numeric(filtered["Quantity"], errors="coerce")

# Create Folium Map
m = folium.Map(location=[filtered.latitude.mean(), filtered.longitude.mean()], zoom_start=8)


# Add points to the map
for _, row in filtered.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,  # Adjust the radius as needed
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.7,
        popup=f"SUBCOUNTY: {row['SUBCOUNTY']}<br>Quantity: {row['Quantity']}",
    ).add_to(m)

folium.LayerControl().add_to(m)

st.subheader(f"Yield Prediction for {selected_year}")
st_folium(m, width=900, height=600)

st.download_button(
    label="Download Yield Data as CSV",
    data=filtered.to_csv(index=False),
    file_name=f"yield_predictions_{selected_year}.csv",
    mime="text/csv"
)