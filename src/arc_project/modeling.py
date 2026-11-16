"""Módulo de modelado MCO (statsmodels OLS), métricas y diagnóstico de residuales."""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import shapiro
from statsmodels.regression.linear_model import RegressionResultsWrapper
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

DEFAULT_PREDICTORS: list[str] = [
    "WURS",
    "Adhd TScore Commissions",
    "ACC__fourier_entropy__bins_100",
    "CT",
]


def fit_ols_model(
    df: pd.DataFrame,
    target: str = "ASRS",
    predictors: list[str] | None = None,
    log_target: bool = False,
) -> tuple[RegressionResultsWrapper, pd.DataFrame]:
    """Ajusta un modelo de regresión lineal múltiple por MCO usando statsmodels."""
    cols = predictors if predictors is not None else DEFAULT_PREDICTORS
    model_df = df[[target, *cols]].dropna().copy()

    y = np.log(model_df[target]) if log_target else model_df[target]
    x = sm.add_constant(model_df[cols])

    model = sm.OLS(y, x).fit()
    return model, model_df


def extract_model_metrics(model: RegressionResultsWrapper) -> dict[str, float | int]:
    """Extrae métricas globales de ajuste del modelo MCO."""
    rmse = float(np.sqrt(np.mean(model.resid**2)))
    return {
        "n_obs": int(model.nobs),
        "r2": float(model.rsquared),
        "r2_adj": float(model.rsquared_adj),
        "f_stat": float(model.fvalue),
        "f_pvalue": float(model.f_pvalue),
        "aic": float(model.aic),
        "bic": float(model.bic),
        "rmse": rmse,
    }


def extract_coefficients_table(model: RegressionResultsWrapper) -> pd.DataFrame:
    """Genera tabla de coeficientes estimados, EE, estadístico t, p-valor e IC 95%."""
    conf = model.conf_int()
    return pd.DataFrame(
        {
            "variable": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "t_stat": model.tvalues.values,
            "p_value": model.pvalues.values,
            "ci_low": conf[0].values,
            "ci_high": conf[1].values,
        }
    )


def run_residual_diagnostics(model: RegressionResultsWrapper) -> dict[str, float]:
    """Ejecuta pruebas de normalidad (Shapiro-Wilk), heterocedasticidad (BP) e independencia (DW)."""
    shapiro_stat, shapiro_p = shapiro(model.resid)
    bp_stat, bp_p, _, _ = het_breuschpagan(model.resid, model.model.exog)
    dw_stat = durbin_watson(model.resid)
    return {
        "shapiro_stat": float(shapiro_stat),
        "shapiro_p": float(shapiro_p),
        "bp_stat": float(bp_stat),
        "bp_p": float(bp_p),
        "durbin_watson": float(dw_stat),
    }


def save_modeling_outputs(
    model: RegressionResultsWrapper,
    vif_df: pd.DataFrame,
    output_dir: Path = Path("reports/tables"),
) -> None:
    """Guarda tablas de coeficientes, métricas globales, diagnósticos y VIF en CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    extract_coefficients_table(model).to_csv(output_dir / "ols_coefficients.csv", index=False)

    metrics = extract_model_metrics(model)
    diagnostics = run_residual_diagnostics(model)
    summary_df = pd.DataFrame([{**metrics, **diagnostics}])
    summary_df.to_csv(output_dir / "ols_summary_metrics.csv", index=False)

    vif_df.to_csv(output_dir / "ols_vif.csv", index=False)
