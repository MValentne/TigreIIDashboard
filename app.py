"""Main Streamlit entry point for the TIGRE II dashboard."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
import subprocess

import streamlit as st

from utils.loader import DEFAULT_DATA_PATH, load_dataset

ROOT_DIR = Path(__file__).resolve().parent


@st.cache_data(show_spinner=False)
def cached_dataset() -> object:
    """Load the Excel dataset once per session."""
    return load_dataset(DEFAULT_DATA_PATH)


def load_page_module(relative_path: str, module_name: str) -> ModuleType:
    """Load a page module whose filename is not a valid Python identifier."""
    page_path = ROOT_DIR / relative_path
    spec = spec_from_file_location(module_name, page_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar el módulo de página: {page_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def open_dataset_file() -> bool:
    """Open the Excel dataset with the default desktop application."""
    try:
        subprocess.Popen(["xdg-open", str(DEFAULT_DATA_PATH)])
    except OSError:
        return False
    return True


def main() -> None:
    """Render the application shell and navigation."""
    st.set_page_config(page_title="TIGRE II - Página principal", page_icon="📊", layout="wide")

    dataset = cached_dataset()
    descriptive_page = load_page_module("pages/1_Descriptivo.py", "page_descriptivo")
    inferential_page = load_page_module("pages/2_Inferencial.py", "page_inferencial")

    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 1.6rem;
                padding-bottom: 2rem;
            }
            .tigre-hero {
                padding: 1.2rem 1.4rem;
                border-radius: 1rem;
                background: linear-gradient(135deg, rgba(17, 24, 39, 0.96), rgba(30, 41, 59, 0.92));
                color: white;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
                margin-bottom: 1rem;
            }
            .tigre-hero h1 {
                margin: 0;
                font-size: 2rem;
                line-height: 1.15;
            }
            .tigre-hero p {
                margin: 0.35rem 0 0;
                opacity: 0.9;
                font-size: 0.98rem;
            }
            div[data-testid="stMetric"] {
                background: rgba(15, 23, 42, 0.03);
                border: 1px solid rgba(15, 23, 42, 0.08);
                padding: 0.75rem 0.9rem;
                border-radius: 0.9rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tigre-hero">
            <h1>Página principal</h1>
            <p>Dashboard interactivo para análisis descriptivo e inferencial basado en Excel.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_metrics = st.columns(4)
    top_metrics[0].metric("Registros", len(dataset))
    top_metrics[1].metric("Variables", 5)
    top_metrics[2].metric("Turnos", dataset["Turno"].nunique())
    top_metrics[3].metric("Satisfacción", dataset["Satisfaccion"].nunique())

    st.divider()

    descriptive_tab, inferential_tab = st.tabs(["Descriptivo", "Inferencial"])

    with st.sidebar:
        st.subheader("Datos")
        st.caption("Abre el archivo para editarlo y recalcular los análisis al volver a cargar la app.")
        if st.button("Abrir Excel", use_container_width=True):
            if not open_dataset_file():
                st.error("No se pudo abrir el archivo Excel con la aplicación del sistema.")
        st.write(f"Archivo: {DEFAULT_DATA_PATH.name}")
        st.write(f"Registros cargados: {len(dataset)}")
        st.write("Columnas: ID, Turno, Satisfaccion, HorasCapacitacion, Ventas")
        st.caption("Los cambios en el Excel se reflejan al recargar la página.")

    with descriptive_tab:
        descriptive_page.render(dataset)

    with inferential_tab:
        inferential_page.render(dataset)


if __name__ == "__main__":
    main()
