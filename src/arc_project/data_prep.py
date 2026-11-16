"""Módulo de carga, limpieza e integración del dataset HYPERAKTIV para ARC."""

from pathlib import Path

import pandas as pd

DEFAULT_RAW_DIR = Path("data/raw")
DEFAULT_PROCESSED_PATH = Path("data/processed/hyperaktiv_arc_clean.csv")


def load_raw_tables(
    raw_dir: Path = DEFAULT_RAW_DIR,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga las tres tablas tabulares crudas de HYPERAKTIV."""
    patients = pd.read_csv(raw_dir / "patient_info.csv", sep=";")
    features = pd.read_csv(raw_dir / "features.csv", sep=";")
    cpt = pd.read_csv(
        raw_dir / "CPT_II_ConnersContinuousPerformanceTest.csv",
        sep=";",
        encoding="utf-8-sig",
    )
    return patients, features, cpt


def integrate_hyperaktiv(
    raw_dir: Path = DEFAULT_RAW_DIR,
    output_path: Path | None = DEFAULT_PROCESSED_PATH,
    max_omissions: int = 300,
) -> pd.DataFrame:
    """Integra patient_info, features y CPT-II mediante inner join por ID.

    Aplica la regla de calidad de datos (Raw Score Omissions < max_omissions),
    elimina IDs duplicados si existieran y descarta filas sin variable respuesta ASRS.
    """
    patients, features, cpt = load_raw_tables(raw_dir)

    # Asegurar unicidad por ID antes del inner join
    patients_clean = patients.drop_duplicates(subset=["ID"]).copy()
    features_clean = features.drop_duplicates(subset=["ID"]).copy()
    cpt_clean = cpt.drop_duplicates(subset=["ID"]).copy()

    # Filtrar sesiones corruptas de CPT-II (desconexión de teclado / sin respuestas)
    cpt_valid = cpt_clean[cpt_clean["Raw Score Omissions"] < max_omissions].copy()

    # Renombrar columnas de métricas agregadas de CPT-II para evitar colisiones
    cpt_summary_cols = [
        col for col in cpt_valid.columns if not col.startswith(("Trial", "Response"))
    ]
    cpt_subset = cpt_valid[cpt_summary_cols]

    merged = (
        patients_clean.merge(cpt_subset, on="ID", how="inner")
        .merge(features_clean, on="ID", how="inner")
        .dropna(subset=["ASRS"])
        .reset_index(drop=True)
    )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        merged.to_csv(output_path, index=False)

    return merged
