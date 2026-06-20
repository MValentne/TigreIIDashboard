"""Load and validate the Excel dataset used by the dashboard."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pandas import DataFrame

REQUIRED_COLUMNS = ["ID", "Turno", "Satisfaccion", "HorasCapacitacion", "Ventas"]
DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "datos.xlsx"


def load_dataset(path: str | Path = DEFAULT_DATA_PATH) -> DataFrame:
    """Load the Excel file and validate its schema."""
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {data_path}")

    dataframe = pd.read_excel(data_path, engine="openpyxl")
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(missing_columns)}")

    dataframe = dataframe[REQUIRED_COLUMNS].copy()
    dataframe["ID"] = pd.to_numeric(dataframe["ID"], errors="raise").astype(int)
    dataframe["Turno"] = dataframe["Turno"].astype(str).str.strip()
    dataframe["Satisfaccion"] = dataframe["Satisfaccion"].astype(str).str.strip()
    dataframe["HorasCapacitacion"] = pd.to_numeric(dataframe["HorasCapacitacion"], errors="raise")
    dataframe["Ventas"] = pd.to_numeric(dataframe["Ventas"], errors="raise")

    if dataframe.isna().any().any():
        raise ValueError("El dataset contiene valores nulos después de la validación.")

    return dataframe
