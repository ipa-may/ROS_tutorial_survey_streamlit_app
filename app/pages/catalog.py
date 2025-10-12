from __future__ import annotations

import pandas as pd
import streamlit as st

from app.data import unique_comma_separated_values
from app.ui.search import GlobalSearch


def show_catalog(dataframe: pd.DataFrame) -> None:
    """Render the main catalog table with global and column filters."""
    search = GlobalSearch()
    query = search.render()
    filtered = search.apply(dataframe, query)

    st.sidebar.header("Filters")
    name_filter = st.sidebar.text_input("Name contains")
    org_filter = st.sidebar.text_input("Organization contains")
    distro_options = unique_comma_separated_values(filtered.get("ros_distro", pd.Series(dtype=str)))
    distro_filter = st.sidebar.multiselect("ROS distro", options=distro_options)

    if name_filter:
        filtered = filtered[filtered["name"].str.contains(name_filter, case=False, na=False)]

    if org_filter and "organization" in filtered.columns:
        filtered = filtered[filtered["organization"].str.contains(org_filter, case=False, na=False)]

    if distro_filter and "ros_distro" in filtered.columns:
        distro_pattern = "|".join(distro_filter)
        filtered = filtered[filtered["ros_distro"].str.contains(distro_pattern, case=False, na=False)]

    display_columns = [column for column in filtered.columns if column != "row_index"]
    st.dataframe(filtered[display_columns], width="stretch", height=600)
