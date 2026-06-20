"""Main Streamlit entry point for the TIGRE II dashboard."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
import subprocess

import streamlit as st

from utils.loader import DEFAULT_DATA_PATH, load_dataset

ROOT_DIR = Path(__file__).resolve().parent


def dataset_fingerprint(path: Path = DEFAULT_DATA_PATH) -> tuple[int, int]:
    """Return a lightweight fingerprint that changes when the Excel changes."""
    stat_result = path.stat()
    return stat_result.st_mtime_ns, stat_result.st_size


@st.cache_data(show_spinner=False)
def cached_dataset(fingerprint: tuple[int, int]) -> object:
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
    st.set_page_config(page_title="TIGRE II - Pagina principal", page_icon="📊", layout="wide")

    fingerprint = dataset_fingerprint()
    dataset = cached_dataset(fingerprint)
    descriptive_page = load_page_module("pages/Descriptivo.py", "page_descriptivo")
    inferential_page = load_page_module("pages/Inferencial.py", "page_inferential")

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

    with st.sidebar:
        st.subheader("Datos")
        st.caption("Abre el archivo para editarlo y recalcular los análisis al volver a cargar la pagina principal.")
        if st.button("Abrir Excel", use_container_width=True):
            if not open_dataset_file():
                st.error("No se pudo abrir el archivo Excel con la aplicación del sistema.")
        if st.button("Refrescar datos", use_container_width=True):
            cached_dataset.clear()
            st.rerun()

        st.write(f"Archivo: {DEFAULT_DATA_PATH.name}")
        st.write(f"Registros cargados: {len(dataset)}")
        st.write("Columnas: ID, Turno, Satisfaccion, HorasCapacitacion, Ventas")
        st.caption("Los cambios en el Excel se reflejan al recargar o refrescar la pagina principal.")

        detail_descriptive_tab, detail_inferential_tab = st.tabs(["Descriptivo", "Inferencial"])
        with detail_descriptive_tab:
            descriptive_page.render_sidebar_details(dataset)
        with detail_inferential_tab:
            inferential_page.render_sidebar_details(dataset)

    main_left, main_right = st.columns([1.15, 0.85])
    with main_left:
        st.subheader("Accesos rápidos")
        st.caption("Usa estas páginas para entrar a las vistas reales del dashboard.")
        st.page_link("pages/Descriptivo.py", label="Abrir Descriptivo", icon="📊")
        st.page_link("pages/Inferencial.py", label="Abrir Inferencial", icon="📈")

    with main_right:
        st.subheader("Vista general")
        st.info("La pagina principal concentra el resumen y el panel lateral mantiene el detalle estadístico completo.")


if __name__ == "__main__":
    main()
