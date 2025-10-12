from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class GlobalSearch:
    """Perform a case-insensitive search across all string columns."""

    placeholder: str = "Search tutorials…"

    def render(self) -> str:
        """Render the Streamlit text input and return the query."""
        import streamlit as st

        return st.text_input("Search", placeholder=self.placeholder)

    def apply(self, dataframe: pd.DataFrame, query: Optional[str]) -> pd.DataFrame:
        """Filter the dataframe to rows containing the query in any column."""
        if not query:
            return dataframe

        lowered = query.lower()
        mask = pd.Series(False, index=dataframe.index)

        for column in dataframe.columns:
            values = dataframe[column]
            if values.dtype == object or pd.api.types.is_string_dtype(values):
                matches = values.astype(str).str.contains(lowered, case=False, na=False)
                mask = mask | matches

        return dataframe[mask]
