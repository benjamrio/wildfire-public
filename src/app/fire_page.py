import streamlit as st
import json
from src.app.data_preprocessing import filter_data
from src.app.visualizations import create_outcome_fig, create_suppression_fig


def selection_menu(df):
    # selecting the dataframe with input parameters (cause, log area range, reports range)
    # input: full dataframe
    # returns: filtered dataframe, fire_id with minimal index (weird) in the filtered dataframe
    st.title("🔥 Fire suppression")

    with st.container(border=True):
        st.header("Filter")
        log_area_range = st.slider("Area (log scale)", 0.0, 7.0, (1.0, 7.0))
        reports_range = st.slider("Number of reports", 1, 150, (50, 150))
        filtered_df = filter_data(df, log_area_range, reports_range, ["all"])
        fire_metric_col, report_number_col = st.columns(2)
        with fire_metric_col:
            st.metric(label="Number of fires", value=filtered_df.fire_id.nunique())
        with report_number_col:
            st.metric(label="Number of reports", value=len(filtered_df))

        st.text("\n\n\n")

        st.header("Select")

        fire_id = filtered_df.fire_id.iloc[0]
        fire_count = filtered_df.fire_id.nunique()
        fire_indices = list(range(fire_count))
        search = st.radio("Search mode", ["Index", "Name", "Fire ID"], horizontal=True)
        idx_col, empty_col = st.columns([2, 3])
        with idx_col:
            if search == "Index":
                selected_fire_index = st.number_input(
                    "Fire Index",
                    min_value=min(fire_indices),
                    max_value=max(fire_indices),
                    value=0,
                )
                # select first element from ordered injective set of fire_ids
                fire_id = filtered_df.fire_id.unique()[selected_fire_index]
                # fire_id = 7235324
            if search == "Name":
                fire_name = st.text_input("Fire Name")
                selected_df = filtered_df[filtered_df.INCIDENT_NAME == fire_name]
                if len(selected_df) > 0:
                    fire_id = selected_df.fire_id.iloc[0]
            if search == "Fire Id":
                temp_fire_id = st.text_input("Fire ID")
                selected_df = filtered_df[filtered_df.fire_id == temp_fire_id]
                if len(selected_df) > 0:
                    fire_id = temp_fire_id
        with empty_col:
            st.empty()
        fire_id_col, fire_name_col = st.columns(2)
        with fire_id_col:
            st.metric(label="Fire ID", value=fire_id)
            try:
                cost = int(
                    filtered_df[
                        filtered_df.fire_id == fire_id
                    ].EST_IM_COST_TO_DATE.max()
                )
            except:
                cost = "Unknown"
            st.metric(label="Total cost ($)", value=cost)
        with fire_name_col:
            fire_name = filtered_df[filtered_df.fire_id == fire_id].INCIDENT_NAME.iloc[
                0
            ]
            st.metric(label="Fire Name", value=fire_name)
            st.metric(
                label="Fatalities",
                value=filtered_df[filtered_df.fire_id == fire_id].FATALITIES.max(),
            )
    return filtered_df, fire_id


def visualizations(df_fire, pers_cols, qty_cols):
    # input: dataframe
    # returns: None, displays changes over times and dataframe

    sum_pers = df_fire[pers_cols].sum()
    sum_pers = sum_pers[sum_pers > 0]
    fig = create_outcome_fig(df_fire)
    st.plotly_chart(fig, use_container_width=True)

    sum_qty = df_fire[qty_cols].sum()
    sum_qty = sum_qty[sum_qty > 0]
    fig = create_suppression_fig(
        df_fire.loc[
            :, list(sum_qty.index) + ["area", "time_to_first_report", "total_personnel"]
        ]
    )
    st.plotly_chart(fig, use_container_width=True)


def display_dataframe(df_fire, pers_cols, qty_cols):
    df_fire.insert(loc=0, column="#", value=list(range(1, len(df_fire) + 1)))
    with st.expander("Show Fire Data"):
        st.write(
            df_fire[
                [
                    "#",
                    "area",
                    "EST_IM_COST_TO_DATE",
                    "FATALITIES",
                    "total_personnel",
                    "STATUS",
                    "time_to_first_report",
                    "date",
                    "cause_id",
                    "REPORT_FROM_DATE",
                    "REPORT_TO_DATE",
                ]
                + pers_cols
                + qty_cols
            ].rename(
                columns={
                    "EST_IM_COST_TO_DATE": "Estimated Cost",
                    "FATALITIES": "Fatalities",
                    "STATUS": "Status",
                    "area": "Area",
                    "cause_id": "Cause",
                }
            )
        )


def dashboard(df, pers_cols, qty_cols):
    # input: dataframe
    # returns: None, displays interactive visualizations

    filter_col, viz_col = st.columns([1, 3], gap="large")
    with filter_col:
        filtered_df, fire_id = selection_menu(df)
    with viz_col:
        df_fire = filtered_df[filtered_df.fire_id == fire_id]
        visualizations(df_fire, pers_cols, qty_cols)
    sum_pers = df_fire[pers_cols].sum()
    sum_pers = sum_pers[sum_pers > 0].index.tolist()
    sum_qty = df_fire[qty_cols].sum()
    sum_qty = sum_qty[sum_qty > 0].index.tolist()
    display_dataframe(df_fire, sum_pers, sum_qty)
