import plotly.graph_objs as go
import plotly.subplots as sp
import plotly.express as px

fire_color = "#D9420B"
personnel_color = "#0D0D0D"
color_circles = [
    "#003f5c",
    "#2f4b7c",
    "#665191",
    "#a05195",
    "#d45087",
    "#f95d6a",
    "#ff7c43",
    "#ffa600",
]


def create_outcome_fig(fire_df):
    fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

    # "true" area
    fig.add_trace(
        go.Scatter(
            x=fire_df["time_to_first_report"],
            y=fire_df["area"],
            name="Area",
            mode="lines",
            marker=None,  # dict(size=5, opacity=0.2, line=dict(width=2, color="DarkSlateGrey")),
            line=dict(width=4, color=fire_color),
        ),
        secondary_y=False,
    )

    # cost
    fig.add_trace(
        go.Scatter(
            x=fire_df["time_to_first_report"],
            y=fire_df["EST_IM_COST_TO_DATE"],
            mode="lines",
            name="Estimated cost to date",
            line=dict(width=3, color="#0D0D0D"),
        ),
        secondary_y=True,
    )
    # # personnel

    # # other area measure
    # fig.add_trace(
    #     go.Scatter(
    #         x=fire_df["time_to_first_report"],
    #         y=fire_df["FATALITIES"],
    #         mode="lines",
    #         name="Fatalities",
    #         marker=dict(size=5, opacity=0.1, line=dict(width=2, color="DarkSlateGrey")),
    #         line=dict(width=5, color="pink"),
    #     ),
    #     secondary_y=True,
    # )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        title_text="Estimated cost to date", secondary_y=True, showgrid=False
    )
    fig.update_yaxes(title_text="Area", secondary_y=False, showgrid=False)

    fig.update_layout(
        title="Total Personnel and Area over Time",
        xaxis_title="Time to First Report",
    )
    return fig


def create_suppression_fig(fire_df):
    fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=fire_df["time_to_first_report"],
            y=fire_df["area"],
            mode="lines",
            name="Area",
            line=dict(width=4, color=fire_color),
            opacity=1,
        ),
        secondary_y=True,
    )
    print(fire_df.columns)
    fig.add_trace(
        go.Scatter(
            x=fire_df["time_to_first_report"],
            y=fire_df["total_personnel"],
            mode="lines",
            name="Total suppression personnel",
            line=dict(width=2, color=personnel_color),
        ),
        secondary_y=False,
    )
    for i, feature in enumerate(fire_df.columns[1:-3]):
        """<extra></extra>rate: %{feature} -%{week_number}<br>Date: %{week}"""
        if feature != "area":
            feature_name = feature.split("_")[1]
        else:
            feature_name = "area"
        fig.add_trace(
            go.Scatter(
                x=fire_df["time_to_first_report"],
                y=fire_df[feature],
                mode="lines",
                name=feature_name,
                line=dict(color=color_circles[i % len(color_circles)]),
            ),
            secondary_y=False,
        )

    fig.update_layout(
        title="Resource quantity over Time, per type",
        xaxis_title="Time to First Report",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(
        title_text="Ressource Type Quantity", secondary_y=False, showgrid=False
    )
    # fig.update_yaxes(title_text="Area", secondary_y=True, showgrid=False)

    return fig
