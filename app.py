"""Main Streamlit entry point for the TIGRE II dashboard."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

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


def main() -> None:
    """Render the application shell and navigation."""
    st.set_page_config(page_title="TIGRE II - Estadística", page_icon="📊", layout="wide")

    dataset = cached_dataset()
    descriptive_page = load_page_module("pages/1_Descriptivo.py", "page_descriptivo")
    inferential_page = load_page_module("pages/2_Inferencial.py", "page_inferencial")

    st.title("TIGRE II - Estadística")
    st.caption("Dashboard interactivo para análisis descriptivo e inferencial basado en Excel.")

    with st.sidebar:
        st.header("Navegación")
        page_choice = st.radio(
            "Selecciona una página",
            ["Página 1 - Análisis Descriptivo", "Página 2 - Análisis Inferencial"],
        )
        st.divider()
        st.subheader("Fuente de datos")
        st.code(str(DEFAULT_DATA_PATH))
        st.write(f"Registros cargados: {len(dataset)}")
        st.write("Columnas: ID, Turno, Satisfaccion, HorasCapacitacion, Ventas")

    if page_choice == "Página 1 - Análisis Descriptivo":
        descriptive_page.render(dataset)
    else:
        inferential_page.render(dataset)


if __name__ == "__main__":
    main()
