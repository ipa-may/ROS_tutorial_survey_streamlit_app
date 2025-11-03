from __future__ import annotations

import pandas as pd
import streamlit as st

from app.charts.factory import ChartFactory


def show_charts(dataframe: pd.DataFrame) -> None:
    """Render aggregated charts for deployment methods and ROS distros."""
    st.sidebar.info("Charts aggregate all tutorials currently loaded.")

    factory = ChartFactory()

    _render_deployment_chart(factory, dataframe.get("deploy_docker", pd.Series(dtype=str)))
    _render_technology_chart(factory, dataframe.get("technology", pd.Series(dtype=str)))
    _render_language_chart(factory, dataframe.get("language", pd.Series(dtype=str)))
    _render_distro_chart(factory, dataframe.get("distro", pd.Series(dtype=str)))


def _render_deployment_chart(factory: ChartFactory, column: pd.Series) -> None:
    """Render the donut chart summarizing deployment methods."""
    st.subheader("Docker Deployment Overview")
    data, spec = factory.deployment_distribution(column)
    if data.empty:
        st.info("No Docker deployment information available.")
        return

    st.vega_lite_chart(data, spec, use_container_width=True)


def _render_technology_chart(factory: ChartFactory, column: pd.Series) -> None:
    """Render the donut chart summarizing robotics technologies."""
    st.subheader("Robotics Technology Distribution")
    data, spec = factory.technology_distribution(column)
    if data.empty:
        st.info("No robotics technology information available.")
        return

    st.vega_lite_chart(data, spec, use_container_width=True)


def _render_language_chart(factory: ChartFactory, column: pd.Series) -> None:
    """Render the donut chart summarizing languages."""
    st.subheader("Language Distribution")
    data, spec = factory.language_distribution(column)
    if data.empty:
        st.info("No language information available.")
        return

    st.vega_lite_chart(data, spec, use_container_width=True)


def _render_distro_chart(factory: ChartFactory, column: pd.Series) -> None:
    """Render the bar chart summarizing ROS distros."""
    st.subheader("ROS Distro Coverage")
    data, spec = factory.distro_distribution(column)
    if data.empty:
        st.info("No ROS distro information available.")
        return

    st.vega_lite_chart(data, spec, use_container_width=True)
