"""Load and validate the Excel dataset used by the dashboard."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from pandas import DataFrame

DEFAULT_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "datos.xlsx"


def load_dataset(path: str | Path = DEFAULT_DATA_PATH) -> DataFrame:
    """Load the Excel file and validate its schema based on column position."""
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {data_path}")

    dataframe = pd.read_excel(data_path, engine="openpyxl")
    if len(dataframe.columns) < 5:
        raise ValueError(f"El dataset debe tener al menos 5 columnas. Encontradas: {len(dataframe.columns)}")

    # We take the first 5 columns to keep the dataset structure consistent
    columns_subset = list(dataframe.columns[:5])
    dataframe = dataframe[columns_subset].copy()

    col_id = columns_subset[0]
    col_cat1 = columns_subset[1]
    col_cat2 = columns_subset[2]
    col_num1 = columns_subset[3]
    col_num2 = columns_subset[4]

    dataframe[col_id] = pd.to_numeric(dataframe[col_id], errors="raise").astype(int)
    dataframe[col_cat1] = dataframe[col_cat1].astype(str).str.strip()
    dataframe[col_cat2] = dataframe[col_cat2].astype(str).str.strip()
    dataframe[col_num1] = pd.to_numeric(dataframe[col_num1], errors="raise")
    dataframe[col_num2] = pd.to_numeric(dataframe[col_num2], errors="raise")

    if dataframe.isna().any().any():
        raise ValueError("El dataset contiene valores nulos después de la validación.")

    return dataframe
