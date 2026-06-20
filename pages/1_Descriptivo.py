"""Descriptive dashboard page."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from stats.chi2 import chi2_test, interpretar_chi2
from stats.correlacion import interpretar_r, pearson
from utils.helpers import format_p_value


def _contingency_bar_chart(contingency: pd.DataFrame) -> go.Figure:
    melted = contingency.reset_index().melt(id_vars=contingency.index.name or "index", var_name="Satisfaccion", value_name="Frecuencia")
    x_col = contingency.index.name or "index"
    figure = px.bar(
        melted,
        x=x_col,
        y="Frecuencia",
        color="Satisfaccion",
        barmode="group",
        title="Frecuencias observadas por turno",
        template="plotly_white",
    )
    figure.update_layout(height=420)
    return figure


def _scatter_regression_chart(dataframe: pd.DataFrame) -> go.Figure:
    figure = px.scatter(
        dataframe,
        x="HorasCapacitacion",
        y="Ventas",
        title="Horas de capacitación vs Ventas",
        template="plotly_white",
    )
    x_values = np.linspace(dataframe["HorasCapacitacion"].min(), dataframe["HorasCapacitacion"].max(), 100)
    slope, intercept = np.polyfit(dataframe["HorasCapacitacion"], dataframe["Ventas"], 1)
    figure.add_trace(
        go.Scatter(
            x=x_values,
            y=intercept + slope * x_values,
            mode="lines",
            name="Línea de regresión",
            line=dict(color="#d62728"),
        )
    )
    figure.update_layout(height=420)
    return figure


def render(dataframe: pd.DataFrame) -> None:
    """Render the descriptive analysis page."""
    st.header("Página 1 - Análisis Descriptivo")
    st.caption("Resultados resumidos para una lectura rápida y no técnica.")

    chi2_result = chi2_test(dataframe)
    correlation_result = pearson(dataframe)

    metric_columns = st.columns(4)
    metric_columns[0].metric("Chi-Cuadrado", f"{chi2_result['chi2']:.2f}")
    metric_columns[1].metric("p-valor", format_p_value(chi2_result["p_value"]))
    metric_columns[2].metric("r", f"{correlation_result['r']:.3f}")
    metric_columns[3].metric("R²", f"{correlation_result['r2']:.3f}")

    st.subheader("Sección Chi-Cuadrado")
    contingency = chi2_result["contingencia"]
    st.dataframe(contingency, use_container_width=True)
    st.plotly_chart(_contingency_bar_chart(contingency), use_container_width=True)
    st.info(interpretar_chi2(chi2_result["p_value"]))

    st.subheader("Sección Correlación")
    st.plotly_chart(_scatter_regression_chart(dataframe), use_container_width=True)
    st.write(f"Coeficiente r: {correlation_result['r']:.3f}")
    st.write(f"R²: {correlation_result['r2']:.3f}")
    st.success(interpretar_r(correlation_result["r"], correlation_result["p_value"]))
