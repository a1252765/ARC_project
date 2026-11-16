"""Módulo de modelado MCO (OLS) y evaluación estadística con statsmodels para ARC."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper

from arc_project.eda import compute_vif


@dataclass
class OLSModelResult:
    """Contenedor estructurado para los resultados de un modelo MCO."""

    target: str
    predictors: list[str]
    n_obs: int
    model: RegressionResultsWrapper
    metrics: dict[str, float]
    coefficients: pd.DataFrame
    vif: pd.DataFrame


def fit_ols_model(
    df: pd.DataFrame,
    predictors: list[str],
    target: str = "ASRS",
) -> OLSModelResult:
    """Ajusta un modelo de Regresión Lineal Múltiple (MCO) con statsmodels.

    Elimina filas con valores faltantes en el objetivo o en los predictores
    seleccionados, añade intercepto y calcula métricas globales, tabla de
    coeficientes con IC al 95% y VIF de los predictores.
    """
    missing_cols = [c for c in [target, *predictors] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Columnas no encontradas en el DataFrame: {missing_cols}")

    df_clean = df[[target, *predictors]].dropna().copy()
    if len(df_clean) <= len(predictors) + 1:
        raise ValueError(
            f"Observaciones insuficientes ({len(df_clean)}) para {len(predictors)} predictores."
        )

    y = df_clean[target]
    x_const = sm.add_constant(df_clean[predictors], has_constant="add")
    fitted = sm.OLS(y, x_const).fit()

    rmse = float(np.sqrt(np.mean(fitted.resid**2)))
    metrics = {
        "n_obs": int(fitted.nobs),
        "r2": float(fitted.rsquared),
        "adj_r2": float(fitted.rsquared_adj),
        "f_stat": float(fitted.fvalue),
        "f_pvalue": float(fitted.f_pvalue),
        "aic": float(fitted.aic),
        "bic": float(fitted.bic),
        "rmse": rmse,
    }

    conf_int = fitted.conf_int(alpha=0.05)
    coefficients = pd.DataFrame(
        {
            "variable": fitted.params.index,
            "coef": fitted.params.values,
            "std_err": fitted.bse.values,
            "t_stat": fitted.tvalues.values,
            "p_value": fitted.pvalues.values,
            "ci_lower": conf_int[0].values,
            "ci_upper": conf_int[1].values,
        }
    )

    vif_df = compute_vif(df_clean, predictors)

    return OLSModelResult(
        target=target,
        predictors=list(predictors),
        n_obs=int(fitted.nobs),
        model=fitted,
        metrics=metrics,
        coefficients=coefficients,
        vif=vif_df,
    )


def save_ols_outputs(
    result: OLSModelResult,
    output_dir: Path = Path("reports/tables"),
    prefix: str = "ols_baseline",
) -> None:
    """Guarda la tabla de coeficientes, VIF y resumen completo del modelo MCO."""
    output_dir.mkdir(parents=True, exist_ok=True)
    result.coefficients.to_csv(output_dir / f"{prefix}_coefficients.csv", index=False)
    result.vif.to_csv(output_dir / f"{prefix}_vif.csv", index=False)
    (output_dir / f"{prefix}_summary.txt").write_text(
        result.model.summary().as_text(),
        encoding="utf-8",
    )

