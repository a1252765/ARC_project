"""Módulo de análisis exploratorio, correlaciones (r) y colinealidad (VIF)."""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant


def compute_target_correlations(
    df: pd.DataFrame,
    target: str = "ASRS",
    min_non_null: int = 30,
    exclude_cols: tuple[str, ...] = ("ID", "ADHD", "ADD", "filter_$"),
) -> pd.DataFrame:
    """Calcula correlación de Pearson (r) y p-valor de cada predictor numérico vs target."""
    if target not in df.columns:
        raise ValueError(f"La columna objetivo '{target}' no existe en el DataFrame.")

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    rows: list[dict[str, float | int | str]] = []

    for col in numeric_cols:
        if col == target or col in exclude_cols:
            continue
        pair = df[[target, col]].dropna()
        if len(pair) < min_non_null or pair[col].nunique() < 2:
            continue
        r_val, p_val = pearsonr(pair[col], pair[target])
        rows.append(
            {
                "variable": col,
                "n": len(pair),
                "r": float(r_val),
                "abs_r": float(abs(r_val)),
                "p_value": float(p_val),
            }
        )

    result = pd.DataFrame(rows).sort_values("abs_r", ascending=False).reset_index(drop=True)
    return result


def compute_vif(df: pd.DataFrame, predictors: list[str]) -> pd.DataFrame:
    """Calcula el Factor de Inflación de Varianza (VIF) para un conjunto de predictores."""
    x_data = df[predictors].dropna()
    x_const = add_constant(x_data)
    vif_rows = []
    for idx, col in enumerate(x_const.columns):
        if col == "const":
            continue
        vif_val = variance_inflation_factor(x_const.values, idx)
        vif_rows.append({"variable": col, "VIF": float(vif_val)})
    return pd.DataFrame(vif_rows)


def save_correlation_table(
    corr_df: pd.DataFrame,
    output_path: Path = Path("reports/tables/top_correlations_asrs.csv"),
    top_n: int = 50,
) -> None:
    """Guarda las top_n variables más correlacionadas con ASRS en CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    corr_df.head(top_n).to_csv(output_path, index=False)
