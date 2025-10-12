from __future__ import annotations

import pandas as pd
import streamlit as st

from app.charts.factory import ChartFactory


def show_charts(dataframe: pd.DataFrame) -> None:
    """Render aggregated charts for deployment methods and ROS distros."""
    st.sidebar.info("Charts aggregate all tutorials currently loaded.")

    factory = ChartFactory()

    _render_deployment_chart(factory, dataframe.get("deployment_docker", pd.Series(dtype=str)))
    _render_robot_type_chart(factory, dataframe.get("robot-type", pd.Series(dtype=str)))
    _render_language_chart(factory, dataframe.get("language", pd.Series(dtype=str)))
    _render_distro_chart(factory, dataframe.get("ros_distro", pd.Series(dtype=str)))


def _render_deployment_chart(factory: ChartFactory, column: pd.Series) -> None:
    """Render the donut chart summarizing deployment methods."""
    st.subheader("Docker Deployment Overview")
    data, spec = factory.deployment_distribution(column)
    if data.empty:
        st.info("No Docker deployment information available.")
        return

    st.vega_lite_chart(data, spec, use_container_width=True)


def _render_robot_type_chart(factory: ChartFactory, column: pd.Series) -> None:
    """Render the donut chart summarizing robot types."""
    st.subheader("Robot Type Distribution")
    data, spec = factory.robot_type_distribution(column)
    if data.empty:
        st.info("No robot type information available.")
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
    data, spec = factory.ros_distro_distribution(column)
    if data.empty:
        st.info("No ROS distro information available.")
        return

    st.vega_lite_chart(data, spec, use_container_width=True)
