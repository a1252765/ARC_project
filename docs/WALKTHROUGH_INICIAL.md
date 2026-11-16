# Walkthrough — Inicialización de `ARC_project`

## Cambios realizados

1. **Repositorio independiente con `uv` y Git:**
   - Inicializado en `/home/richie/Documents/GitHub/ARC_project` (rama `main`, Python `3.13`).
   - Dependencias instaladas con `uv`: `pandas`, `numpy`, `statsmodels`, `scipy`, `matplotlib`, `seaborn` y grupo `dev` (`jupyter`, `ipykernel`, `ruff`).
   - Configurado [.gitignore](file:///home/richie/Documents/GitHub/ARC_project/.gitignore) para excluir `.venv/`, cachés y todos los `.csv` en `data/raw/` y `data/processed/` (los datos se comparten por Google Drive).
   - Documentado en [README.md](file:///home/richie/Documents/GitHub/ARC_project/README.md) el flujo de instalación en Ubuntu con `uv` para Mariana, la división por roles y las reglas de ramas/PRs en GitHub.

2. **Módulos y pipeline inicial:**
   - [data_prep.py](file:///home/richie/Documents/GitHub/ARC_project/src/arc_project/data_prep.py): `load_raw_tables()` e `integrate_hyperaktiv()` integran `patient_info.csv`, `features.csv` y `CPT_II_ConnersContinuousPerformanceTest.csv` por `ID`, filtrando `Raw Score Omissions < 300` y eliminando nulos en `ASRS`.
   - [eda.py](file:///home/richie/Documents/GitHub/ARC_project/src/arc_project/eda.py): `compute_target_correlations()`, `compute_vif()` y `save_correlation_table()`.
   - [run_pipeline.py](file:///home/richie/Documents/GitHub/ARC_project/scripts/run_pipeline.py): ejecuta la integración y exporta las top 50 correlaciones con `ASRS`.

## Validación y resultados observados

- `uv run ruff check src/ scripts/`: **All checks passed!**
- `uv run python scripts/run_pipeline.py`:
  - Dataset integrado guardado en `data/processed/hyperaktiv_arc_clean.csv` con **`n = 75` pacientes** y **885 columnas** (supera el mínimo requerido de $n \ge 30$).
  - Rango de `ASRS`: `6.0` a `68.0` (media = `41.39`, DE = `13.90`).
  - Top correlaciones con `ASRS` guardadas en `reports/tables/top_correlations_asrs.csv`:
    - `WURS` ($n = 74$, $r = 0.6850$, $p = 1.69 \times 10^{-11}$)
    - `Adhd TScore Commissions` ($n = 75$, $r = 0.5280$, $p = 1.13 \times 10^{-6}$)
    - `Adhd TScore DPrime` ($n = 75$, $r = 0.4046$, $p = 3.17 \times 10^{-4}$)
    - `Adhd Confidence Index` ($n = 75$, $r = 0.3443$, $p = 2.49 \times 10^{-3}$)
    - `ACC__fourier_entropy__bins_100` ($n = 75$, $r = 0.3215$, $p = 4.92 \times 10^{-3}$)
