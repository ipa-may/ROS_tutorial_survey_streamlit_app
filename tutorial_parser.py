from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd
import yaml


class TutorialListParser:
    """Load tutorial metadata from YAML into a pandas DataFrame."""

    def __init__(self, source: str | Path) -> None:
        self.source = Path(source)

    def load_dataframe(self) -> pd.DataFrame:
        """Return the tutorials as a pandas DataFrame."""
        records = self._load_yaml()
        normalized = [self._normalize_record(item, index) for index, item in enumerate(records)]
        return pd.DataFrame(normalized)

    def _load_yaml(self) -> list[dict[str, Any]]:
        """Load and validate the YAML content."""
        if not self.source.exists():
            raise FileNotFoundError(f"YAML file not found: {self.source}")

        with self.source.open("r", encoding="utf-8") as handle:
            content = yaml.safe_load(handle)

        if content is None:
            return []

        if not isinstance(content, list):
            raise ValueError("Expected top-level YAML sequence of tutorial entries.")

        cleaned: list[dict[str, Any]] = []
        for index, entry in enumerate(content):
            if not isinstance(entry, Mapping):
                raise ValueError(f"Tutorial entry at index {index} must be a mapping.")
            cleaned.append(dict(entry))

        return cleaned

    def _normalize_record(self, record: Mapping[str, Any], index: int) -> dict[str, Any]:
        """Produce a dict with display-friendly values."""
        normalized: dict[str, Any] = {}
        for key, value in record.items():
            if key == "doc-link":
                normalized["doc_link"] = self._normalize_value(value)
            elif key == "repo-link":
                normalized["repo_link"] = self._normalize_value(value)
            else:
                normalized[key] = self._normalize_value(value)

        # Provide a stable identifier to help when the YAML omits unique keys.
        normalized.setdefault("row_index", index)
        return normalized

    def _normalize_value(self, value: Any) -> Any:
        """Convert nested structures into strings for DataFrame readability."""
        if isinstance(value, Mapping):
            return json.dumps(value, ensure_ascii=False, sort_keys=True)

        if isinstance(value, Iterable) and not isinstance(value, (str, bytes, bytearray)):
            return ", ".join(str(item) for item in value)

        return value


def load_tutorials(path: str | Path) -> pd.DataFrame:
    """Convenience function for loading the tutorials file."""
    return TutorialListParser(path).load_dataframe()
