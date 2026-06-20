# Informe Técnico

## Objetivo

Desarrollar un dashboard estadístico interactivo para la materia Estadística II con carga desde Excel, análisis descriptivo e inferencial y visualizaciones automáticas.

## Arquitectura

- `data/datos.xlsx` contiene la fuente de verdad.
- `utils/loader.py` valida y carga el dataset.
- `stats/` concentra la lógica estadística reutilizable.
- `pages/` separa la experiencia descriptiva e inferencial.
- `app.py` resuelve la navegación y el arranque de la aplicación.

## Resultados

- Se implementó Chi-Cuadrado para `Turno` y `Satisfaccion`.
- Se implementó correlación de Pearson y regresión lineal para `HorasCapacitacion` y `Ventas`.
- Se incluyeron predicción, intervalo de confianza, intervalo de predicción y validación de residuos.

## Validación

- La carga del Excel funciona.
- Los módulos estadísticos devuelven resultados consistentes sobre el dataset.
- Streamlit arranca correctamente con `streamlit run app.py`.
