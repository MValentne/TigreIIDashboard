"""Pearson correlation helpers."""

from __future__ import annotations

from pandas import DataFrame
from scipy.stats import pearsonr

from utils.helpers import strength_label, trend_label


def pearson(
    dataframe: DataFrame,
    x_col: str = "HorasCapacitacion",
    y_col: str = "Ventas",
) -> dict[str, float]:
    """Compute Pearson correlation and its significance."""
    clean = dataframe[[x_col, y_col]].dropna()
    coefficient, p_value = pearsonr(clean[x_col], clean[y_col])
    return {
        "r": float(coefficient),
        "p_value": float(p_value),
        "r2": float(coefficient**2),
        "n": float(len(clean)),
    }


def interpretar_r(r_value: float, p_value: float | None = None, alpha: float = 0.05) -> str:
    """Return a natural-language interpretation of Pearson's r."""
    strength = strength_label(r_value)
    trend = trend_label(r_value)
    base = f"La relación es {strength} y {trend}."
    if p_value is None:
        return base
    significance = "estadísticamente significativa" if p_value < alpha else "no estadísticamente significativa"
    return f"{base} La correlación es {significance}."
