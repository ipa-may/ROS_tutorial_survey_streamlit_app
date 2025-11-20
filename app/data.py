from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from tutorial_parser import load_tutorials


DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "tutorial_list.yaml"


@st.cache_data(show_spinner=False)
def load_app_data(path: Path | None = None) -> pd.DataFrame:
    """Load tutorial metadata from YAML and cache it for the session."""
    target = path or DEFAULT_DATA_PATH
    return load_tutorials(target)


def prepare_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with friendly dtypes for display and filtering."""
    prepared = dataframe.copy()

    if "date" in prepared.columns:
        prepared["date"] = pd.to_numeric(prepared["date"], errors="coerce").astype("Int16")

    object_columns = prepared.select_dtypes(include=["object"]).columns
    for column in object_columns:
        prepared[column] = prepared[column].fillna("").astype(str)

    return prepared


def unique_comma_separated_values(column: pd.Series) -> list[str]:
    """Extract unique values from a comma-separated column."""
    values: set[str] = set()
    for entry in column.dropna():
        for part in str(entry).split(","):
            normalized = part.strip()
            if normalized and normalized.lower() != "not-defined":
                values.add(normalized)
    return sorted(values)


def value_counts_from_column(column: pd.Series) -> pd.DataFrame:
    """Count occurrences of values from a comma-separated column."""
    collected: list[str] = []
    for entry in column.dropna():
        for part in str(entry).split(","):
            normalized = part.strip()
            if normalized and normalized.lower() != "not-defined":
                collected.append(normalized)

    if not collected:
        return pd.DataFrame(columns=["value", "count"])

    counts = pd.Series(collected).value_counts().reset_index()
    counts.columns = ["value", "count"]
    return counts
