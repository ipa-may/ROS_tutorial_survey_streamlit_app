from __future__ import annotations

import streamlit as st

from app.data import DEFAULT_DATA_PATH, load_app_data, prepare_dataframe
from app.pages.catalog import show_catalog
from app.pages.charts import show_charts


def main() -> None:
    st.set_page_config(page_title="ROS Tutorial Survey", layout="wide")
    st.title("ROS Tutorial Survey")
    st.caption("Data sourced from `tutorial_list.yaml`.")

    try:
        dataframe = load_app_data(DEFAULT_DATA_PATH)
    except FileNotFoundError:
        st.error(f"Could not find the YAML file at {DEFAULT_DATA_PATH}.")
        st.stop()
    except Exception as error:
        st.exception(error)
        st.stop()

    if dataframe.empty:
        st.warning("No tutorials available to display.")
        st.stop()

    dataframe = prepare_dataframe(dataframe)

    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Select view", options=("Catalog", "Charts"), index=0)

    if page == "Catalog":
        show_catalog(dataframe)
    else:
        show_charts(dataframe)


if __name__ == "__main__":
    main()
