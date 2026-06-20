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
from utils.loader import load_dataset


@st.cache_data(show_spinner=False)
def _load_dataset() -> pd.DataFrame:
    return load_dataset()


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


def _chi2_detail_frame(contingency: pd.DataFrame, expected: pd.DataFrame) -> pd.DataFrame:
    details = []
    for row_label in contingency.index:
        for column_label in contingency.columns:
            observed = float(contingency.loc[row_label, column_label])
            expected_value = float(expected.loc[row_label, column_label])
            contribution = (observed - expected_value) ** 2 / expected_value if expected_value else 0.0
            details.append(
                {
                    "Turno": row_label,
                    "Satisfaccion": column_label,
                    "Observado": observed,
                    "Esperado": expected_value,
                    "Contribución": contribution,
                }
            )
    return pd.DataFrame(details)


def _pearson_detail_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    clean = dataframe[["HorasCapacitacion", "Ventas"]].dropna().copy()
    clean["dx"] = clean["HorasCapacitacion"] - clean["HorasCapacitacion"].mean()
    clean["dy"] = clean["Ventas"] - clean["Ventas"].mean()
    clean["dx2"] = clean["dx"] ** 2
    clean["dy2"] = clean["dy"] ** 2
    clean["dx_dy"] = clean["dx"] * clean["dy"]
    return clean


def render_sidebar_details(dataframe: pd.DataFrame) -> None:
    """Render the detailed descriptive process inside the sidebar."""
    chi2_result = chi2_test(dataframe)
    correlation_result = pearson(dataframe)
    expected = chi2_result["frecuencias_esperadas"]
    contingency = chi2_result["contingencia"]

    st.markdown("#### Descriptivo")
    st.caption("Paso a paso para reproducir los resultados de la página principal.")

    with st.expander("Chi-Cuadrado: proceso completo", expanded=True):
        st.write("1. Se cruza la variable cualitativa `Turno` con `Satisfaccion`.")
        st.dataframe(contingency, use_container_width=True)
        st.write("2. Se calculan los totales por fila y columna para obtener las frecuencias esperadas.")
        st.dataframe(expected, use_container_width=True)
        st.write("3. Se mide la contribución de cada celda al estadístico final.")
        st.dataframe(_chi2_detail_frame(contingency, expected), use_container_width=True)
        st.write(f"Chi-Cuadrado total: {chi2_result['chi2']:.4f}")
        st.write(f"Grados de libertad: {chi2_result['dof']}")
        st.write(f"p-valor: {format_p_value(chi2_result['p_value'])}")

    with st.expander("Pearson: proceso completo", expanded=True):
        detail_frame = _pearson_detail_frame(dataframe)
        st.write("1. Se toman `HorasCapacitacion` y `Ventas` como variables numéricas.")
        st.write("2. Se calculan medias, desviaciones respecto de la media y productos cruzados.")
        st.dataframe(detail_frame, use_container_width=True)
        numerator = float(detail_frame["dx_dy"].sum())
        denominator = float(np.sqrt(detail_frame["dx2"].sum() * detail_frame["dy2"].sum()))
        st.write(f"Suma de productos cruzados: {numerator:.4f}")
        st.write(f"Raíz del producto de sumas cuadráticas: {denominator:.4f}")
        st.write(f"Coeficiente r: {correlation_result['r']:.4f}")
        st.write(f"R²: {correlation_result['r2']:.4f}")
        st.success(interpretar_r(correlation_result["r"], correlation_result["p_value"]))


def render(dataframe: pd.DataFrame) -> None:
    """Render the descriptive analysis page."""
    st.set_page_config(page_title="TIGRE II - Descriptivo", page_icon="📊", layout="wide")
    st.header("Página principal - Análisis Descriptivo")
    st.caption("Resultados resumidos para una lectura rápida y no técnica.")

    chi2_result = chi2_test(dataframe)
    correlation_result = pearson(dataframe)

    with st.container(border=True):
        metric_columns = st.columns(4)
        metric_columns[0].metric("Chi-Cuadrado", f"{chi2_result['chi2']:.2f}")
        metric_columns[1].metric("p-valor", format_p_value(chi2_result["p_value"]))
        metric_columns[2].metric("r", f"{correlation_result['r']:.3f}")
        metric_columns[3].metric("R²", f"{correlation_result['r2']:.3f}")

    chi2_left, chi2_right = st.columns([1.1, 1])
    contingency = chi2_result["contingencia"]
    with chi2_left:
        with st.container(border=True):
            st.subheader("Sección Chi-Cuadrado")
            st.dataframe(contingency, use_container_width=True)
            st.info(interpretar_chi2(chi2_result["p_value"]))
    with chi2_right:
        with st.container(border=True):
            st.subheader("Frecuencias observadas")
            st.plotly_chart(_contingency_bar_chart(contingency), use_container_width=True)

    with st.container(border=True):
        st.subheader("Sección Correlación")
        st.plotly_chart(_scatter_regression_chart(dataframe), use_container_width=True)
        cor_left, cor_right = st.columns(2)
        cor_left.metric("Coeficiente r", f"{correlation_result['r']:.3f}")
        cor_right.metric("R²", f"{correlation_result['r2']:.3f}")
        st.success(interpretar_r(correlation_result["r"], correlation_result["p_value"]))


if __name__ == "__main__":
    st.set_page_config(page_title="TIGRE II - Descriptivo", page_icon="📊", layout="wide")
    dataset = _load_dataset()
    with st.sidebar:
        render_sidebar_details(dataset)
    render(dataset)
