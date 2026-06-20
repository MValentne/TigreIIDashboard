"""Linear regression helpers based on statsmodels."""

from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
from pandas import DataFrame
from statsmodels.regression.linear_model import RegressionResultsWrapper


def ajustar_modelo(
    dataframe: DataFrame,
    x_col: str = "HorasCapacitacion",
    y_col: str = "Ventas",
) -> RegressionResultsWrapper:
    """Fit a simple linear regression model."""
    clean = dataframe[[x_col, y_col]].dropna().copy()
    X = sm.add_constant(clean[[x_col]])
    y = clean[y_col]
    modelo = sm.OLS(y, X).fit()
    return modelo


def _prediction_frame(modelo: RegressionResultsWrapper, horas: float, alpha: float = 0.05) -> DataFrame:
    """Build a one-row prediction frame for a given number of training hours."""
    new_data = pd.DataFrame({"HorasCapacitacion": [horas]})
    new_data = sm.add_constant(new_data, has_constant="add")
    return modelo.get_prediction(new_data).summary_frame(alpha=alpha)


def prediccion(modelo: RegressionResultsWrapper, horas: float, alpha: float = 0.05) -> dict[str, float]:
    """Return a point prediction with confidence and prediction intervals."""
    summary = _prediction_frame(modelo, horas, alpha=alpha).iloc[0]
    return {
        "venta_esperada": float(summary["mean"]),
        "intervalo_confianza_inferior": float(summary["mean_ci_lower"]),
        "intervalo_confianza_superior": float(summary["mean_ci_upper"]),
        "intervalo_prediccion_inferior": float(summary["obs_ci_lower"]),
        "intervalo_prediccion_superior": float(summary["obs_ci_upper"]),
    }


def intervalo_confianza(modelo: RegressionResultsWrapper, horas: float, alpha: float = 0.05) -> tuple[float, float]:
    """Return the confidence interval for the mean predicted value."""
    summary = _prediction_frame(modelo, horas, alpha=alpha).iloc[0]
    return float(summary["mean_ci_lower"]), float(summary["mean_ci_upper"])


def intervalo_prediccion(modelo: RegressionResultsWrapper, horas: float, alpha: float = 0.05) -> tuple[float, float]:
    """Return the prediction interval for a new observation."""
    summary = _prediction_frame(modelo, horas, alpha=alpha).iloc[0]
    return float(summary["obs_ci_lower"]), float(summary["obs_ci_upper"])
