# CONTEXT.md

# TIGRE II - Estadística

## Dashboard Interactivo de Análisis Estadístico

---

# Objetivo General

Desarrollar un dashboard estadístico interactivo para la materia Estadística II.

El sistema debe permitir:

* Cargar datos desde Excel.
* Modificar datos fácilmente.
* Actualizar automáticamente todos los análisis.
* Realizar análisis descriptivos e inferenciales.
* Implementar pruebas Chi-Cuadrado.
* Implementar Correlación y Regresión Lineal.
* Mostrar gráficos e interpretaciones automáticas.
* Mantener una arquitectura simple y mantenible.

El resultado final debe ser un proyecto funcional listo para presentar académicamente.

---

# Filosofía del Proyecto

Priorizar:

1. Simplicidad.
2. Mantenibilidad.
3. Facilidad de uso.
4. Robustez estadística.
5. Facilidad de demostración.

NO utilizar bases de datos.

La fuente de verdad será un archivo Excel.

---

# Stack Tecnológico Obligatorio

## Lenguaje

Python 3.12+

---

## Dashboard

Streamlit

---

## Manipulación de datos

pandas
numpy

---

## Estadística

scipy
statsmodels

---

## Gráficos

plotly

---

## Lectura de Excel

openpyxl

---

# Arquitectura Objetivo

TIGRE-II/

data/
│
└── datos.xlsx

docs/
│
├── CONTEXT.md
├── prompts.md
└── informe.md

stats/
│
├── chi2.py
├── correlacion.py
├── regresion.py
└── validacion.py

utils/
│
├── loader.py
└── helpers.py

pages/
│
├── 1_Descriptivo.py
└── 2_Inferencial.py

app.py

requirements.txt

README.md

---

# Fuente de Datos

Utilizar exclusivamente:

data/datos.xlsx

Toda la aplicación debe recalcular automáticamente cuando cambie el Excel.

No utilizar SQLite.

No utilizar PostgreSQL.

No utilizar MySQL.

No utilizar APIs externas.

---

# Dataset Objetivo

La base debe contener variables cualitativas y cuantitativas.

Variables mínimas:

ID
Turno
Satisfaccion
HorasCapacitacion
Ventas

Ejemplo:

ID | Turno | Satisfaccion | HorasCapacitacion | Ventas

1 | Mañana | Alta | 12 | 105
2 | Tarde | Media | 8 | 88
3 | Noche | Baja | 4 | 55

Cantidad recomendada:

50 registros.

---

# Página 1 - Análisis Descriptivo

Objetivo:

Mostrar resultados para usuarios no técnicos.

---

## Sección Chi-Cuadrado

Variables:

Turno
Satisfaccion

Mostrar:

* Tabla de contingencia.
* Frecuencias observadas.
* Gráfico de barras.
* Valor Chi-Cuadrado.
* p-valor.
* Interpretación automática.

---

## Sección Correlación

Variables:

HorasCapacitacion
Ventas

Mostrar:

* Scatterplot.
* Línea de regresión.
* Coeficiente r.
* R².
* Interpretación automática.

---

# Página 2 - Análisis Inferencial

Objetivo:

Mostrar el detalle estadístico.

---

## Sección Chi-Cuadrado

Mostrar:

* Hipótesis H0.
* Hipótesis H1.
* Frecuencias observadas.
* Frecuencias esperadas.
* Chi-Cuadrado calculado.
* Grados de libertad.
* p-valor.
* Decisión.
* Conclusión textual.

---

## Sección Regresión

Mostrar:

* Ecuación estimada.
* Pendiente.
* Intercepto.
* Estadístico t.
* p-valor.
* Intervalos de confianza.
* R².

---

## Predicción

Permitir ingresar:

HorasCapacitacion

Mostrar:

* Venta esperada.
* Intervalo de confianza.
* Intervalo de predicción.

---

# Validación de Supuestos

Implementar:

## Residuos vs Ajustados

## Histograma de residuos

## QQ Plot

Mostrar conclusiones automáticas.

---

# Módulos Estadísticos

## chi2.py

Implementar:

* tabla_contingencia()
* frecuencias_esperadas()
* chi2_test()
* interpretar_chi2()

---

## correlacion.py

Implementar:

* pearson()
* interpretar_r()

---

## regresion.py

Implementar:

* ajustar_modelo()
* prediccion()
* intervalo_confianza()
* intervalo_prediccion()

---

## validacion.py

Implementar:

* residuos()
* qqplot()
* histograma_residuos()

---

# Requisitos de Calidad

El código debe:

* Tener type hints.
* Tener docstrings.
* Ser modular.
* Ser reutilizable.
* Evitar duplicación.
* Mantener separación clara entre lógica y visualización.

---

# Diseño UI

Preferencias:

* Diseño limpio.
* Dos páginas.
* Sidebar para navegación.
* Métricas destacadas arriba.
* Gráficos Plotly.

Evitar:

* Diseño recargado.
* Temas extravagantes.
* Dependencias innecesarias.

---

# Gestión del Progreso

El agente debe actualizar esta sección cada vez que complete una tarea.

## Estado General

Proyecto:
[ ] No iniciado
[x] En desarrollo
[x] Finalizado

---

## Infraestructura

[x] Crear estructura de carpetas
[x] Crear requirements.txt
[x] Crear README.md
[x] Crear CONTEXT.md

---

## Datos

[x] Diseñar dataset
[x] Crear datos.xlsx
[x] Implementar loader.py
[ ] Validar carga de datos

---

## Estadística

### Chi Cuadrado

[x] Tabla de contingencia
[x] Frecuencias esperadas
[x] Prueba Chi-Cuadrado
[x] Interpretación automática

### Correlación

[x] Pearson
[x] Interpretación de r

### Regresión

[x] Ajuste de modelo
[x] Predicción
[x] Intervalos de confianza
[x] Intervalos de predicción

### Validación

[x] Residuos
[x] Histograma
[x] QQ Plot

---

## Dashboard

### Página 1

[x] Tabla de contingencia
[x] Barras
[x] Scatterplot
[x] Métricas

### Página 2

[x] Frecuencias esperadas
[x] Hipótesis
[x] Regresión detallada
[x] Predicciones

---

## Testing

[x] Verificación de carga Excel
[x] Verificación Chi-Cuadrado
[x] Verificación Pearson
[x] Verificación Regresión
[x] Verificación UI

---

## Documentación

[x] README
[x] Informe técnico
[x] Registro de prompts

---

# Criterio de Finalización

El proyecto se considera terminado cuando:

* El dashboard ejecuta correctamente.
* Los datos provienen de Excel.
* Todas las estadísticas funcionan.
* Las visualizaciones son correctas.
* Las interpretaciones se generan automáticamente.
* El progreso marca todas las tareas completadas.
* La aplicación puede ejecutarse mediante:

streamlit run app.py

sin errores.

FIN DEL CONTEXTO
