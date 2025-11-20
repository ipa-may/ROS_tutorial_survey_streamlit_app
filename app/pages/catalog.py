from __future__ import annotations

import re

import pandas as pd
import streamlit as st

from app.data import unique_comma_separated_values
from app.ui.search import GlobalSearch

CATALOG_COLUMN_ORDER = [
    "name",
    "organization",
    "date",
    "governance",
    "country",
    "maintainer",
    "user",
    "intro",
    "doc",
    "doc_type",
    "language",
    "technology",
    "application",
    "robot",
    "hardware",
    "stack",
    "repo",
    "packages",
    "distro",
    "deploy_native",
    "deploy_gui",
    "deploy_specifics",
    "deploy_docker",
    "docker_image_base",
    "docker_overlay",
    "ci",
]

COLUMN_HELP_TEXT = {
    "name": "Description of the Training Material.",
    "organization": "Owner of the Material.",
    "date": "Creation or last major update year.",
    "governance": "[company, consortium, laboratory, university, community, individual] governance type.",
    "country": "[de, us, es, fr, gb, it] country of origin.",
    "maintainer": "Contact of known expert contributors or maintainers.",
    "user": "Contact of known trainers or users.",
    "intro": "Introduction page to the Material (e.g., ROS Discourse).",
    "doc": "Documentation URL (e.g., https://robgineer.github.io/cobot/).",
    "doc_type": "[pdf, sphinx, markdown, workshop repository] documentation format.",
    "language": "[de, en, es, fr, gb, it] languages covered by the Material.",
    "technology": "[manipulation, navigation, perception, software-engineering, fieldbus] robotics technology focus.",
    "application": "[welding, pickplace, palletizing, conveying, humanoid] robotics application focus.",
    "robot": "[ur5e, ur10e, panda, pcobot, scara, turtlebot3] robots covered by the Material.",
    "hardware": "[stm32_f407, raspberry_pi4, jetson_nano, nvidia_gpu, tof_vl53l1x] additional hardware required.",
    "stack": "[basics, ros2_control, urdf, gazebo, rviz, moveit, nav2, tesseract, opencv, pytorch] software stack coverage.",
    "repo": "Code repository URL (e.g., https://github.com/robgineer/cobot).",
    "packages": "Software packages covered by the Material.",
    "distro": "[humble, jazzy, rolling, windows10, debian12] ROS distro or specific OS supported.",
    "deploy_native": "[bash, ansible, iso, fai] native deployment method.",
    "deploy_gui": "[x11local, x11forward, tigervnc, webapp] method to display ROS GUI.",
    "deploy_specifics": "[devcontainer, virtualbox, clusterssh] deployment specifics.",
    "deploy_docker": "[dockerfile, dockercompose, rocker, ade] Docker deployment approach.",
    "docker_image_base": "Base Docker image (e.g., tiryoh/ros2-desktop-vnc:jazzy).",
    "docker_overlay": "[builder, dever, visualizer] Docker overlay type.",
    "ci": "Continuous integration availability (true/false).",
}


def _options_from_column(column: pd.Series) -> list[str]:
    return sorted({str(value) for value in column.dropna() if str(value)})


def _apply_contains_filter(
    dataframe: pd.DataFrame, column: str, selections: list[str]
) -> pd.DataFrame:
    if selections and column in dataframe.columns:
        pattern = "|".join(re.escape(selection) for selection in selections)
        return dataframe[dataframe[column].str.contains(pattern, case=False, na=False)]
    return dataframe


def _apply_exact_filter(dataframe: pd.DataFrame, column: str, selections: list[str]) -> pd.DataFrame:
    if selections and column in dataframe.columns:
        normalized = {str(selection) for selection in selections}
        return dataframe[dataframe[column].astype(str).isin(normalized)]
    return dataframe


def show_catalog(dataframe: pd.DataFrame) -> None:
    """Render the main catalog table with global and column filters."""
    search = GlobalSearch()
    query = search.render()
    filtered = search.apply(dataframe, query)

    st.sidebar.header("Filters")
    name_filter = st.sidebar.text_input("Name contains")
    org_filter = st.sidebar.text_input("Organization contains")
    distro_options = unique_comma_separated_values(filtered.get("distro", pd.Series(dtype=str)))
    distro_filter = st.sidebar.multiselect("ROS distro", options=distro_options)
    tech_options = unique_comma_separated_values(filtered.get("technology", pd.Series(dtype=str)))
    tech_filter = st.sidebar.multiselect("Technology", options=tech_options)
    application_options = unique_comma_separated_values(filtered.get("application", pd.Series(dtype=str)))
    application_filter = st.sidebar.multiselect("Application", options=application_options)
    stack_options = unique_comma_separated_values(filtered.get("stack", pd.Series(dtype=str)))
    stack_filter = st.sidebar.multiselect("Stack", options=stack_options)
    robot_options = unique_comma_separated_values(filtered.get("robot", pd.Series(dtype=str)))
    robot_filter = st.sidebar.multiselect("Robot", options=robot_options)
    hardware_options = unique_comma_separated_values(filtered.get("hardware", pd.Series(dtype=str)))
    hardware_filter = st.sidebar.multiselect("Hardware", options=hardware_options)
    deploy_docker_options = unique_comma_separated_values(filtered.get("deploy_docker", pd.Series(dtype=str)))
    deploy_docker_filter = st.sidebar.multiselect("Deploy (Docker)", options=deploy_docker_options)
    deploy_gui_options = unique_comma_separated_values(filtered.get("deploy_gui", pd.Series(dtype=str)))
    deploy_gui_filter = st.sidebar.multiselect("Deploy (GUI)", options=deploy_gui_options)
    governance_options = _options_from_column(filtered.get("governance", pd.Series(dtype=str)))
    governance_filter = st.sidebar.multiselect("Governance", options=governance_options)
    date_options = _options_from_column(filtered.get("date", pd.Series(dtype=str)))
    date_filter = st.sidebar.multiselect("Date", options=date_options)
    language_options = unique_comma_separated_values(filtered.get("language", pd.Series(dtype=str)))
    language_filter = st.sidebar.multiselect("Language", options=language_options)

    if name_filter:
        filtered = filtered[filtered["name"].str.contains(name_filter, case=False, na=False)]

    if org_filter and "organization" in filtered.columns:
        filtered = filtered[filtered["organization"].str.contains(org_filter, case=False, na=False)]

    filtered = _apply_contains_filter(filtered, "distro", distro_filter)
    filtered = _apply_contains_filter(filtered, "technology", tech_filter)
    filtered = _apply_contains_filter(filtered, "application", application_filter)
    filtered = _apply_contains_filter(filtered, "stack", stack_filter)
    filtered = _apply_contains_filter(filtered, "robot", robot_filter)
    filtered = _apply_contains_filter(filtered, "hardware", hardware_filter)
    filtered = _apply_contains_filter(filtered, "deploy_docker", deploy_docker_filter)
    filtered = _apply_contains_filter(filtered, "deploy_gui", deploy_gui_filter)
    filtered = _apply_contains_filter(filtered, "language", language_filter)
    filtered = _apply_exact_filter(filtered, "governance", governance_filter)
    filtered = _apply_exact_filter(filtered, "date", date_filter)

    if "legacy" in filtered.columns:
        non_legacy_mask = ~filtered["legacy"].astype(str).str.lower().eq("true")
        filtered = filtered[non_legacy_mask]

    ordered_columns = [column for column in CATALOG_COLUMN_ORDER if column in filtered.columns]
    remaining_columns = [
        column
        for column in filtered.columns
        if column not in ordered_columns and column not in {"row_index", "legacy"}
    ]
    display_columns = ordered_columns + remaining_columns
    column_config: dict[str, st.column_config.Column] = {}
    for column in display_columns:
        help_text = COLUMN_HELP_TEXT.get(column)
        if column == "doc":
            kwargs: dict[str, str] = {"help": help_text} if help_text else {}
            column_config[column] = st.column_config.LinkColumn("Documentation", **kwargs)
        elif column == "repo":
            kwargs = {"help": help_text} if help_text else {}
            column_config[column] = st.column_config.LinkColumn("Repository", **kwargs)
        elif help_text:
            label = column.replace("_", " ").title()
            column_config[column] = st.column_config.Column(label, help=help_text)

    st.dataframe(
        filtered[display_columns],
        width="stretch",
        height=600,
        column_config=column_config if column_config else None,
    )
