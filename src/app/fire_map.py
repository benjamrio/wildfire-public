import plotly.graph_objs as go
import plotly.subplots as sp
import plotly.express as px
import streamlit as st
import pandas as pd

st


def fire_map(df):
    # define one viz level (zipcode?)
    # aggregate values there.. large wildfires??
    # especially: where are people allocated to? try to find a pattern throughout time
    # => test in jupyter (get one static picture per month)
    map_fig = display_map(df)
    st.plotly_chart(map_fig, use_container_width=True)


@st.cache_data
def display_map(df):
    df["date"] = pd.to_datetime(df[["year", "month", "day"]])
    df = df.sort_values("date")
    fig = px.scatter_geo(
        df,
        lon="POO_LONGITUDE",
        lat="POO_LATITUDE",
        color="total_personnel",
        projection="natural earth",
        animation_frame="date",
    )  # or "mercator", "orthographic", etc.
    fig.update_layout(
        mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return fig
