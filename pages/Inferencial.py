"""Inferential dashboard page."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy.stats import shapiro

from stats.chi2 import chi2_test, interpretar_chi2
from stats.regresion import ajustar_modelo, intervalo_confianza, intervalo_prediccion, prediccion
from stats.validacion import conclusiones_residuos, histograma_residuos, qqplot, residuos_vs_ajustados
from utils.helpers import format_p_value, regression_equation
from utils.loader import load_dataset


@st.cache_data(show_spinner=False)
def _load_dataset() -> pd.DataFrame:
    return load_dataset()


def _equation_text(modelo) -> str:
    intercept = float(modelo.params["const"])
    slope = float(modelo.params["HorasCapacitacion"])
    return regression_equation(intercept, slope)


def _regression_summary_frame(modelo) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Coeficiente": ["Intercepto", "Pendiente"],
            "Valor": [float(modelo.params["const"]), float(modelo.params["HorasCapacitacion"])],
            "t": [float(modelo.tvalues["const"]), float(modelo.tvalues["HorasCapacitacion"])],
            "p-valor": [float(modelo.pvalues["const"]), float(modelo.pvalues["HorasCapacitacion"])],
        }
    )


def _residual_summary_frame(modelo) -> pd.DataFrame:
    residuals = pd.Series(modelo.resid, name="residuos")
    _, shapiro_p = shapiro(residuals)
    return pd.DataFrame(
        {
            "Métrica": ["Media", "Desviación estándar", "Mínimo", "Máximo", "Shapiro p-valor"],
            "Valor": [
                float(residuals.mean()),
                float(residuals.std(ddof=1)),
                float(residuals.min()),
                float(residuals.max()),
                shapiro_p,
            ],
        }
    )


def render_sidebar_details(dataframe: pd.DataFrame) -> None:
    """Render the detailed inferential process inside the sidebar."""
    chi2_result = chi2_test(dataframe)
    modelo = ajustar_modelo(dataframe)
    slope = float(modelo.params["HorasCapacitacion"])
    intercept = float(modelo.params["const"])

    st.markdown("#### Inferencial")
    st.caption("Desglose estadístico para reproducir los resultados de la página principal.")

    with st.expander("Chi-Cuadrado inferencial", expanded=False):
        st.markdown("**H0:** Turno y Satisfaccion son independientes.")
        st.markdown("**H1:** Turno y Satisfaccion no son independientes.")
        st.write("Tabla observada:")
        st.dataframe(chi2_result["contingencia"], use_container_width=True)
        st.write("Tabla esperada:")
        st.dataframe(chi2_result["frecuencias_esperadas"], use_container_width=True)
        st.write(f"Chi-Cuadrado: {chi2_result['chi2']:.4f}")
        st.write(f"Gl: {chi2_result['dof']}")
        st.write(f"p-valor: {format_p_value(chi2_result['p_value'])}")

    with st.expander("Regresión lineal", expanded=False):
        st.write(f"Ecuación: {regression_equation(intercept, slope)}")
        st.dataframe(_regression_summary_frame(modelo), use_container_width=True)
        coef_interval = modelo.conf_int().loc["HorasCapacitacion"]
        st.write(f"Intervalo de confianza de la pendiente: [{coef_interval.iloc[0]:.4f}, {coef_interval.iloc[1]:.4f}]")
        st.write(f"R²: {modelo.rsquared:.4f}")

    with st.expander("Predicción", expanded=False):
        horas_sidebar = st.number_input(
            "Horas para predecir",
            min_value=0.0,
            value=float(dataframe["HorasCapacitacion"].mean()),
            step=0.5,
            key="sidebar_prediction_hours",
        )
        prediction = prediccion(modelo, horas_sidebar)
        st.metric("Venta esperada", f"{prediction['venta_esperada']:.2f}")
        st.write(f"IC: [{prediction['intervalo_confianza_inferior']:.2f}, {prediction['intervalo_confianza_superior']:.2f}]")
        st.write(f"IP: [{prediction['intervalo_prediccion_inferior']:.2f}, {prediction['intervalo_prediccion_superior']:.2f}]")

    with st.expander("Validación de supuestos", expanded=False):
        st.write("Residuos resumidos:")
        st.dataframe(_residual_summary_frame(modelo), use_container_width=True)
        st.info(conclusiones_residuos(modelo))


def render(dataframe: pd.DataFrame) -> None:
    """Render the inferential analysis page."""
    st.header("Página 2 - Análisis Inferencial")
    st.caption("Detalle estadístico, prueba formal y predicción del modelo lineal.")

    chi2_result = chi2_test(dataframe)
    modelo = ajustar_modelo(dataframe)

    chi2_left, chi2_right = st.columns([1.05, 0.95])
    with chi2_left:
        with st.container(border=True):
            st.subheader("Sección Chi-Cuadrado")
            st.markdown("**H0:** Turno y Satisfaccion son independientes.")
            st.markdown("**H1:** Turno y Satisfaccion no son independientes.")
            st.dataframe(chi2_result["contingencia"], use_container_width=True)
            st.dataframe(chi2_result["frecuencias_esperadas"], use_container_width=True)
    with chi2_right:
        with st.container(border=True):
            st.subheader("Resumen")
            st.metric("Chi-Cuadrado", f"{chi2_result['chi2']:.4f}")
            st.metric("p-valor", format_p_value(chi2_result['p_value']))
            st.write(f"Grados de libertad: {chi2_result['dof']}")
            st.write(f"Decisión: {'Rechazar H0' if chi2_result['p_value'] < 0.05 else 'No rechazar H0'}")
            st.success(interpretar_chi2(chi2_result["p_value"]))

    with st.container(border=True):
        st.subheader("Sección Regresión")
        st.write(f"Ecuación estimada: {_equation_text(modelo)}")
        st.dataframe(_regression_summary_frame(modelo), use_container_width=True)
        coef_interval = modelo.conf_int().loc["HorasCapacitacion"]
        st.write(f"R²: {modelo.rsquared:.4f}")
        st.write(f"Intervalo de confianza del coeficiente de pendiente: [{coef_interval.iloc[0]:.4f}, {coef_interval.iloc[1]:.4f}]")

    with st.container(border=True):
        st.subheader("Predicción")
        horas = st.number_input("Horas de capacitación", min_value=0.0, value=float(dataframe["HorasCapacitacion"].mean()), step=0.5)
        prediction = prediccion(modelo, horas)
        ci_low, ci_high = intervalo_confianza(modelo, horas)
        pi_low, pi_high = intervalo_prediccion(modelo, horas)
        prediction_columns = st.columns(3)
        prediction_columns[0].metric("Venta esperada", f"{prediction['venta_esperada']:.2f}")
        prediction_columns[1].metric("IC", f"[{ci_low:.2f}, {ci_high:.2f}]")
        prediction_columns[2].metric("IP", f"[{pi_low:.2f}, {pi_high:.2f}]")

    with st.container(border=True):
        st.subheader("Validación de Supuestos")
        st.plotly_chart(residuos_vs_ajustados(modelo), use_container_width=True)
        st.plotly_chart(histograma_residuos(modelo), use_container_width=True)
        st.plotly_chart(qqplot(modelo), use_container_width=True)
        st.info(conclusiones_residuos(modelo))


if __name__ == "__main__":
    st.set_page_config(page_title="TIGRE II - Inferencial", page_icon="📈", layout="wide")
    dataset = _load_dataset()
    with st.sidebar:
        render_sidebar_details(dataset)
    render(dataset)
