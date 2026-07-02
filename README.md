# TIGRE II - Estadística

Dashboard interactivo para la materia Estadística II, construido con Python 3.12+ y Streamlit.

## Características

- Carga de datos desde `data/datos.xlsx`.
- Análisis descriptivo con Chi-Cuadrado y correlación de Pearson.
- Análisis inferencial con Chi-Cuadrado, regresión lineal y predicción.
- Visualizaciones con Plotly.
- Validación básica de supuestos mediante residuos, histograma y QQ Plot.

## Estructura

- `app.py`: punto de entrada principal.
- `data/datos.xlsx`: fuente de verdad del dashboard.
- `stats/`: lógica estadística reutilizable.
- `utils/`: carga y funciones auxiliares.
- `pages/`: lógica de cada vista del dashboard.
- `docs/`: documentación complementaria.

## Ejecución

Instala dependencias y ejecuta:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notas
- Link del video explicativo de la aplicación (https://drive.google.com/file/d/1TlSAK9b4Pc8UWnzT6iA0T86PkjwmX8Mg/view?usp=sharing)
- No se usa base de datos.
- Si cambias `data/datos.xlsx`, la aplicación recalcula los análisis al recargar.
