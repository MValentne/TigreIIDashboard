"""Chi-square analysis helpers."""

from __future__ import annotations

import pandas as pd
from pandas import DataFrame
from scipy.stats import chi2_contingency

from utils.helpers import interpret_significance


def tabla_contingencia(
    dataframe: DataFrame,
    fila: str = "Turno",
    columna: str = "Satisfaccion",
) -> DataFrame:
    """Build the contingency table for two categorical variables."""
    return pd.crosstab(dataframe[fila], dataframe[columna])


def frecuencias_esperadas(contingencia: DataFrame) -> DataFrame:
    """Compute the expected frequencies for a contingency table."""
    _, _, _, expected = chi2_contingency(contingencia)
    return pd.DataFrame(expected, index=contingencia.index, columns=contingencia.columns)


def chi2_test(
    dataframe: DataFrame,
    fila: str = "Turno",
    columna: str = "Satisfaccion",
) -> dict[str, object]:
    """Run the Chi-square test of independence."""
    contingencia = tabla_contingencia(dataframe, fila=fila, columna=columna)
    chi2_statistic, p_value, degrees_of_freedom, expected = chi2_contingency(contingencia)
    expected_frame = pd.DataFrame(expected, index=contingencia.index, columns=contingencia.columns)

    return {
        "contingencia": contingencia,
        "frecuencias_esperadas": expected_frame,
        "chi2": float(chi2_statistic),
        "p_value": float(p_value),
        "dof": int(degrees_of_freedom),
    }


def interpretar_chi2(p_value: float, alpha: float = 0.05) -> str:
    """Return a short natural-language conclusion for the Chi-square test."""
    if p_value < alpha:
        return f"Existe asociación estadísticamente significativa entre las variables. {interpret_significance(p_value, alpha)}"
    return f"No se observa evidencia suficiente de asociación entre las variables. {interpret_significance(p_value, alpha)}"
