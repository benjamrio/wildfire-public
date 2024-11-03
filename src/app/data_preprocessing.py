import pandas as pd
import numpy as np
import json


def load_data(file_path):
    return pd.read_csv(file_path, index_col=0, low_memory=False)


def filter_data(df, log_area_range, reports_range, cause):
    # Select cause, select range for fire area and nb of reports (almost like nb of days - sometimes way longer)
    min_area, max_area = np.power(10, log_area_range)
    min_reports, max_reports = reports_range
    # Cause
    if "all" not in cause:
        causes = [int(c) for c in cause]
        df = df[df.cause_id.notna()]
        df = df[df["cause_id"].astype(int).isin(causes)]

    # Fire size
    fire_sizes = df.groupby("fire_id").size()
    long_fires = fire_sizes[(fire_sizes >= min_reports) & (fire_sizes <= max_reports)]
    df = df[df.fire_id.isin(long_fires.index)]

    # Fire area
    fire_max_area = df.groupby("fire_id")["area"].max()
    large_fires = fire_max_area[
        (fire_max_area >= min_area) & (fire_max_area <= max_area)
    ]
    df = df[df.fire_id.isin(large_fires.index)]

    return df
