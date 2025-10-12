from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd

from app.data import value_counts_from_column

ROS_DISTRO_ORDER = [
    "kinetic",
    "melodic",
    "noetic",
    "foxy",
    "galactic",
    "humble",
    "iron",
    "jazzy",
    "kilted",
    "rolling",
]


@dataclass(frozen=True)
class ChartFactory:
    """Produce Vega-Lite specifications for catalog charts."""

    pie_width: int = 500
    pie_height: int = 500
    inner_radius: int = 50
    outer_radius: int = 200

    def deployment_distribution(self, column: pd.Series) -> tuple[pd.DataFrame, dict]:
        """Return data and spec for the deployment distribution donut chart."""
        return self._donut_distribution(column, title="Deployment")

    def robot_type_distribution(self, column: pd.Series) -> tuple[pd.DataFrame, dict]:
        """Return data and spec for the robot-type donut chart."""
        return self._donut_distribution(column, title="Robot Type")

    def language_distribution(self, column: pd.Series) -> tuple[pd.DataFrame, dict]:
        """Return data and spec for the language donut chart."""
        return self._donut_distribution(column, title="Language")

    def ros_distro_distribution(self, column: pd.Series) -> tuple[pd.DataFrame, dict]:
        """Return data and spec for the ROS distro bar chart."""
        counts = value_counts_from_column(column)
        if counts.empty:
            return counts, {}

        order = self._resolve_distro_order(counts["value"].tolist())
        spec = {
            "mark": {"type": "bar"},
            "encoding": {
                "x": {
                    "field": "value",
                    "type": "nominal",
                    "title": "ROS Distro",
                    "sort": order,
                },
                "y": {"field": "count", "type": "quantitative", "title": "Tutorials"},
                "tooltip": [
                    {"field": "value", "type": "nominal", "title": "ROS Distro"},
                    {"field": "count", "type": "quantitative"},
                ],
                "color": {"field": "value", "type": "nominal", "legend": None},
            },
        }
        return counts, spec

    def _resolve_distro_order(self, values: Iterable[str]) -> list[str]:
        """Return a stable ordering that prioritises known ROS distros."""
        values_list = list(values)
        desired = [name for name in ROS_DISTRO_ORDER if name in values_list]
        remaining = sorted(name for name in values_list if name not in desired)
        return desired + remaining

    def _donut_distribution(self, column: pd.Series, *, title: str) -> tuple[pd.DataFrame, dict]:
        """Shared builder for donut-style categorical charts."""
        counts = value_counts_from_column(column)
        if counts.empty:
            return counts, {}

        spec = {
            "width": self.pie_width,
            "height": self.pie_height,
            "mark": {
                "type": "arc",
                "innerRadius": self.inner_radius,
                "outerRadius": self.outer_radius,
            },
            "encoding": {
                "theta": {"field": "count", "type": "quantitative"},
                "color": {
                    "field": "value",
                    "type": "nominal",
                    "title": title,
                    "legend": {"labelFontSize": 22, "titleFontSize": 20, "orient": "left", "offset": -20},
                },
                "tooltip": [
                    {"field": "value", "type": "nominal", "title": title},
                    {"field": "count", "type": "quantitative"},
                ],
            },
        }
        return counts, spec
