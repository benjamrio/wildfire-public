import streamlit as st
import pickle
from src.app.fire_page import dashboard
from src.app.fire_map import fire_map
from src.app.data_preprocessing import load_data

sit_path = "data/preprocessed/final_dataset.csv"
df = load_data(sit_path)
with open("data/preprocessed/features.pkl", "rb") as f:
    treatment_features_personnel, treatment_features_qty = pickle.load(f)

st.set_page_config(
    page_title="Wildfire-lab",
    page_icon="🔥",
    layout="wide",
)

# st.sidebar.title("Naviguate")
# page = st.sidebar.selectbox("Choose a page", ["One Fire Dashboard", "Mutlifire Map"])

# if page == "One Fire Dashboard":
dashboard(df, treatment_features_personnel, treatment_features_qty)
# elif page == "Mutlifire Map":
#    fire_map(df)
