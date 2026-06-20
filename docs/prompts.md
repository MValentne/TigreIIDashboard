# Registro de Prompts

## 2026-06-20

- Objetivo: construir un dashboard estadístico interactivo para Estadística II tomando `context.md` como fuente principal.
- Decisiones: usar `data/datos.xlsx` como única fuente de verdad, sin base de datos ni APIs externas.
- Estructura creada: `data/`, `docs/`, `stats/`, `utils/`, `pages/`, `app.py` y `requirements.txt`.
- Validaciones realizadas: carga del Excel, cálculo de Chi-Cuadrado, correlación de Pearson, regresión lineal y arranque de Streamlit.
