"""Regression assumption checks and visualizations."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import probplot, shapiro
from statsmodels.regression.linear_model import RegressionResultsWrapper


def residuos(modelo: RegressionResultsWrapper) -> pd.Series:
    """Return model residuals."""
    return pd.Series(modelo.resid, name="residuos")


def residuos_vs_ajustados(modelo: RegressionResultsWrapper) -> go.Figure:
    """Plot residuals against fitted values."""
    fitted = pd.Series(modelo.fittedvalues, name="ajustados")
    residual_series = residuos(modelo)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=fitted,
            y=residual_series,
            mode="markers",
            name="Residuos",
            marker=dict(color="#1f77b4", size=10),
        )
    )
    figure.add_hline(y=0, line_dash="dash", line_color="#444")
    figure.update_layout(
        title="Residuos vs Ajustados",
        xaxis_title="Valores ajustados",
        yaxis_title="Residuos",
        template="plotly_white",
        height=420,
    )
    return figure


def qqplot(modelo: RegressionResultsWrapper) -> go.Figure:
    """Build a QQ plot for model residuals."""
    residual_series = residuos(modelo)
    theoretical, ordered = probplot(residual_series, dist="norm", fit=False)
    slope, intercept, _ = probplot(residual_series, dist="norm", fit=True)[1]

    lower = min(np.min(theoretical), np.min(ordered))
    upper = max(np.max(theoretical), np.max(ordered))

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=theoretical,
            y=ordered,
            mode="markers",
            name="Residuos observados",
            marker=dict(color="#ff7f0e", size=9),
        )
    )
    figure.add_trace(
        go.Scatter(
            x=[lower, upper],
            y=[intercept + slope * lower, intercept + slope * upper],
            mode="lines",
            name="Referencia normal",
            line=dict(color="#1f77b4"),
        )
    )
    figure.update_layout(
        title="QQ Plot de Residuos",
        xaxis_title="Cuantiles teóricos",
        yaxis_title="Cuantiles de residuos",
        template="plotly_white",
        height=420,
    )
    return figure


def histograma_residuos(modelo: RegressionResultsWrapper) -> go.Figure:
    """Plot a histogram of the residuals."""
    residual_series = residuos(modelo)
    figure = go.Figure()
    figure.add_trace(
        go.Histogram(
            x=residual_series,
            nbinsx=12,
            name="Residuos",
            marker_color="#2ca02c",
            opacity=0.8,
        )
    )
    figure.update_layout(
        title="Histograma de Residuos",
        xaxis_title="Residuo",
        yaxis_title="Frecuencia",
        template="plotly_white",
        height=420,
    )
    return figure


def conclusiones_residuos(modelo: RegressionResultsWrapper) -> str:
    """Return a short heuristic conclusion about residual normality."""
    residual_series = residuos(modelo)
    shapiro_stat, shapiro_p = shapiro(residual_series)
    if shapiro_p >= 0.05:
        return f"Los residuos no muestran evidencia fuerte contra la normalidad (Shapiro-Wilk p = {shapiro_p:.4f})."
    return f"Los residuos sugieren una desviación de la normalidad (Shapiro-Wilk p = {shapiro_p:.4f})."
