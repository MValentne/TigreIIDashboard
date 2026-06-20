"""Inferential dashboard page."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from stats.chi2 import chi2_test, interpretar_chi2
from stats.regresion import ajustar_modelo, intervalo_confianza, intervalo_prediccion, prediccion
from stats.validacion import conclusiones_residuos, histograma_residuos, qqplot, residuos_vs_ajustados
from utils.helpers import format_p_value, regression_equation


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


def render(dataframe: pd.DataFrame) -> None:
    """Render the inferential analysis page."""
    st.header("Página 2 - Análisis Inferencial")
    st.caption("Detalle estadístico, prueba formal y predicción del modelo lineal.")

    chi2_result = chi2_test(dataframe)
    modelo = ajustar_modelo(dataframe)

    st.subheader("Sección Chi-Cuadrado")
    st.markdown("**H0:** Turno y Satisfaccion son independientes.")
    st.markdown("**H1:** Turno y Satisfaccion no son independientes.")
    st.dataframe(chi2_result["contingencia"], use_container_width=True)
    st.dataframe(chi2_result["frecuencias_esperadas"], use_container_width=True)
    st.write(f"Chi-Cuadrado calculado: {chi2_result['chi2']:.4f}")
    st.write(f"Grados de libertad: {chi2_result['dof']}")
    st.write(f"p-valor: {format_p_value(chi2_result['p_value'])}")
    st.write(f"Decisión: {'Rechazar H0' if chi2_result['p_value'] < 0.05 else 'No rechazar H0'}")
    st.success(interpretar_chi2(chi2_result["p_value"]))

    st.subheader("Sección Regresión")
    st.write(f"Ecuación estimada: {_equation_text(modelo)}")
    st.dataframe(_regression_summary_frame(modelo), use_container_width=True)
    st.write(f"R²: {modelo.rsquared:.4f}")
    st.write(f"Intervalo de confianza del coeficiente de pendiente: [{modelo.conf_int().loc['HorasCapacitacion', 0]:.4f}, {modelo.conf_int().loc['HorasCapacitacion', 1]:.4f}]")

    st.subheader("Predicción")
    horas = st.number_input("Horas de capacitación", min_value=0.0, value=float(dataframe["HorasCapacitacion"].mean()), step=0.5)
    prediction = prediccion(modelo, horas)
    ci_low, ci_high = intervalo_confianza(modelo, horas)
    pi_low, pi_high = intervalo_prediccion(modelo, horas)
    st.metric("Venta esperada", f"{prediction['venta_esperada']:.2f}")
    st.write(f"Intervalo de confianza: [{ci_low:.2f}, {ci_high:.2f}]")
    st.write(f"Intervalo de predicción: [{pi_low:.2f}, {pi_high:.2f}]")

    st.subheader("Validación de Supuestos")
    st.plotly_chart(residuos_vs_ajustados(modelo), use_container_width=True)
    st.plotly_chart(histograma_residuos(modelo), use_container_width=True)
    st.plotly_chart(qqplot(modelo), use_container_width=True)
    st.info(conclusiones_residuos(modelo))
