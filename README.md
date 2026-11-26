# Modelado de la Severidad de Síntomas de TDAH en Adultos (`ASRS`) mediante Regresión Lineal Múltiple (MCO)

**Universidad Autónoma de Baja California (UABC)** — Licenciatura en Ciencia de Datos  
**Materia:** Análisis de Regresión y Correlación (ARC)  
**Profesora:** Cynthia Calderón García  
**Autores:** Luis Alejandro Luna Martínez & Mariana Salazar  

- **Reporte técnico completo (con desarrollo matemático en LaTeX):** [reports/reporte_final/reporte_final_arc.pdf](reports/reporte_final/reporte_final_arc.pdf)
- **Bitácora original de desarrollo:** [docs/BITACORA_GUIA_DESARROLLO.md](docs/BITACORA_GUIA_DESARROLLO.md)
- **Metodología CRISP-ML(Q):** [docs/METODOLOGIA_CRISP_ML.md](docs/METODOLOGIA_CRISP_ML.md)

---

## 1. Acerca del Proyecto

Este repositorio contiene un flujo reproducible de ciencia de datos que modela la severidad autorreportada de síntomas de Trastorno por Déficit de Atención e Hiperactividad (TDAH) en adultos (`ASRS`) mediante **Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO)** sobre el conjunto de datos clínico **HYPERAKTIV** (Hicks et al., 2021).

Se utilizó regresión lineal múltiple (y no series de tiempo) debido a que los datos son de **corte transversal** (cada registro corresponde a un paciente evaluado en una sola sesión clínica, sin orden cronológico ni mediciones repetidas). Todo el desarrollo sigue el marco **CRISP-ML(Q)** dividido en cuatro cuadernos secuenciales.

---

## 2. Dataset y Diccionario de Variables

Los datos provienen del estudio clínico abierto **HYPERAKTIV** (licencia original CC BY-NC 4.0, disponible en https://datasets.simula.no/hyperaktiv/). Por respeto a su licencia, los archivos `.csv` no se incluyen en este repositorio; abajo se explica cómo descargarlos y ubicarlos para replicar el análisis.

### Archivos crudos requeridos (`data/raw/`)

| Archivo | Separador / Codificación | Contenido principal |
|---|---|---|
| `patient_info.csv` | `;` / `utf-8` | Demografía, diagnósticos clínicos y escalas autorreportadas (`ASRS`, `WURS`, `MADRS`, `HADS_A`, `HADS_D`) |
| `features.csv` | `;` / `utf-8` | Características estadísticas derivadas de actigrafía motora y variabilidad cardiaca (HRV) |
| `CPT_II_ConnersContinuousPerformanceTest.csv` | `;` / `utf-8-sig` | Métricas neuropsicológicas objetivas de atención sostenida e impulsividad (CPT-II) |

### Variables del modelo final (`n = 69` casos completos)

| Rol | Variable | Instrumento | Escala / Rango | Qué mide e interpretación clínica |
|---|---|---|---|---|
| **Objetivo (Y)** | `ASRS` | Adult ADHD Self-Report Scale v1.1 (OMS) | Continua (`0–72`) | Severidad actual autorreportada de síntomas de TDAH en adultos (18 ítems DSM). Mayor puntaje = mayor severidad. |
| **Predictor (X1)** | `WURS` | Wender Utah Rating Scale | Continua (`0–100`) | Síntomas retrospectivos de TDAH en la infancia. Valores `≥ 46` son punto de corte orientativo de TDAH infantil. |
| **Predictor (X2)** | `General TScore Commissions` | Conners' CPT-II | Puntaje T (media `50`, DE `10`) | Errores de comisión en prueba computarizada (responder cuando se debía inhibir). Mide impulsividad objetiva (`T > 60` elevado). |
| **Predictor (X3)** | `HADS_A` | Hospital Anxiety and Depression Scale | Continua (`0–21`) | Sintomatología de ansiedad comórbida (`0–7` normal, `8–10` limítrofe, `≥ 11` clínicamente significativa). |

### Variables excluidas deliberadamente y justificación

- **Excluidas por fuga de información (*data leakage*):** `ID` (identificador) y los diagnósticos binarios directos `ADHD` y `ADD`, ya que equivalen al diagnóstico mismo.
- **Descartadas en el EDA y selección:**
  - `General TScore DPrime`: alta colinealidad con `General TScore Commissions` (`r = 0.88`).
  - `General TScore Omissions`: correlación inflada (`r = 0.287`) por un único valor extremo (`≈ 330`).
  - `MADRS`, `HADS_D` y `AGE`: sin correlación lineal significativa con `ASRS` (`p > 0.15`).
  - Columnas de detalle ensayo por ensayo del CPT-II: eliminadas durante la limpieza para conservar únicamente métricas agregadas.

---

## 3. Estructura del Repositorio

```text
ARC_project/
├── data/
│   ├── raw/                                     # Colocar aquí los 3 CSV originales de HYPERAKTIV (ignorado en Git)
│   └── processed/                               # Salida limpia generada por el Notebook 01 (hyperaktiv_arc_clean.csv)
├── notebooks/
│   ├── 01_data_ingestion_and_cleaning.ipynb     # Ingesta, regla CPT-II (Omissions < 300), inner join por ID (n = 75)
│   ├── 02_eda_and_feature_selection.ipynb       # Distribución de ASRS, Pearson r, dispersiones y validación VIF (n = 69)
│   ├── 03_ols_modeling_and_diagnostics.ipynb    # Ajuste MCO, pruebas F/t, real vs. predicho y diagnóstico de residuales
│   └── 04_transformations_and_forecasting.ipynb # Comparación de transformaciones (ln, sqrt, parsimonioso) y pronósticos
├── reports/
│   ├── figures/                                 # 5 gráficas oficiales exportadas en PNG (150 dpi)
│   ├── tables/                                  # 7 tablas oficiales en CSV (correlaciones, VIF, MCO, diagnóstico, pronósticos)
│   └── reporte_final/
│       ├── reporte_final_arc.pdf                # Reporte final compilado en LaTeX (13 páginas)
│       ├── reporte_final_arc.tex                # Código fuente LaTeX del reporte
│       └── reporte_final_arc.md                 # Versión Markdown unificada
├── src/arc_project/                             # Módulos Python reutilizables (data_prep, eda, modeling)
├── docs/
│   ├── BITACORA_GUIA_DESARROLLO.md              # Guía operativa original y reparto de fases
│   ├── METODOLOGIA_CRISP_ML.md                  # Trazabilidad por fase CRISP-ML(Q)
│   └── GUION_EXPOSICION.md                      # Guion de defensa oral (12–15 min) y banco de Q&A
├── pyproject.toml                               # Dependencias y metadatos del proyecto (Python 3.13)
└── uv.lock                                      # Lockfile reproducible de uv
```

---

## 4. Cómo Replicar el Proyecto Paso a Paso

### Requisitos previos
- Python `3.13`
- Gestor de entornos y paquetes [`uv`](https://docs.astral.sh/uv/) (instalable con `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Paso 1: Clonar el repositorio e instalar dependencias
```bash
git clone https://github.com/a1252765/ARC_project.git
cd ARC_project
uv sync
```

### Paso 2: Descargar y colocar los datos de HYPERAKTIV
1. Descarga el dataset desde https://datasets.simula.no/hyperaktiv/ (o OSF: https://osf.io/3agwr/).
2. Copia únicamente los tres archivos tabulares en `data/raw/`:
   - `data/raw/patient_info.csv`
   - `data/raw/features.csv`
   - `data/raw/CPT_II_ConnersContinuousPerformanceTest.csv`

### Paso 3: Ejecutar los notebooks en orden
Abre Jupyter Lab usando el entorno sincronizado:
```bash
uv run jupyter lab
```

Ejecuta los cuatro cuadernos en orden secuencial:
1. `notebooks/01_data_ingestion_and_cleaning.ipynb` → genera `data/processed/hyperaktiv_arc_clean.csv` (`75 × 885`).
2. `notebooks/02_eda_and_feature_selection.ipynb` → exporta `asrs_distribucion.png`, `dispersion_candidatas.png`, `correlaciones_asrs.csv` y `ols_vif.csv`.
3. `notebooks/03_ols_modeling_and_diagnostics.ipynb` → exporta `ols_coefficients.csv`, `ols_summary_metrics.csv`, `ols_diagnostics.csv`, `ols_real_vs_predicho.png` y `ols_residual_diagnostics.png`.
4. `notebooks/04_transformations_and_forecasting.ipynb` → exporta `ols_transformations_comparison.csv`, `ols_forecasts.csv` y `ols_forecasts_profiles.png`.

---

## 5. Resumen de Resultados Principales

**Ecuación estimada por MCO (`n = 69`):**
```text
ASRS_hat = 7.6350 + 0.3678 * WURS + 0.3079 * Commissions + 0.1273 * HADS_A
```

| Indicador | Resultado | Interpretación |
|---|---|---|
| `R²` / `R² ajustado` | `0.5341` / `0.5126` | Explica el 53.41 % de la variabilidad de `ASRS` (`RMSE = 9.90`) |
| Prueba `F(3, 65)` | `24.8355` (`p = 8.00e-11`) | Modelo globalmente significativo (`p < 0.001`) |
| Multicolinealidad (`VIF`) | `1.623`, `1.390`, `1.205` | Todos `< 5` (ausencia de multicolinealidad) |
| Normalidad (Shapiro-Wilk) | `W = 0.9780` (`p = 0.2634`) | Cumple normalidad (`α = 0.05`) |
| Homocedasticidad (Breusch-Pagan) | `LM = 6.7705` (`p = 0.0796`) | Cumple homocedasticidad (`α = 0.05`) |
| Independencia (Durbin-Watson) | `DW = 2.174` | Sin autocorrelación |
| Transformaciones (`ln`, `sqrt`, sin `HADS_A`) | Descartadas | El modelo lineal base es el único que cumple todos los supuestos y minimiza el `RMSE` (`9.6102`) |

**Pronósticos en tres perfiles clínicos (percentiles P10, P50 y P90, sin extrapolación):**

| Perfil clínico | `WURS` | `Commissions` | `HADS_A` | `ASRS` predicho | IC 95 % (media) | IP 95 % (individual) |
|---|---:|---:|---:|---:|---|---|
| Carga baja (P10) | 16 | 43 | 3 | **27.14** | `[22.48, 31.81]` | `[6.82, 47.46]` |
| Carga moderada (P50) | 38 | 57 | 9 | **40.31** | `[37.90, 42.72]` | `[20.39, 60.23]` |
| Carga alta (P90) | 65 | 73 | 16 | **56.06** | `[51.11, 61.00]` | `[35.67, 72.00]` *(acotado a 72)* |

---

## 6. Referencias (APA 7.ª edición)

Conners, C. K. (2000). *Conners' Continuous Performance Test II (CPT II) computer program for Windows technical guide and software manual*. Multi-Health Systems.

Hicks, S. A., Stautland, A., Fasmer, O. B., Førland, W., Hammer, H. L., Halvorsen, P., Mjeldheim, K., Oedegaard, K. J., Osnes, B., Syrstad, V. E. G., Riegler, M. A., & Jakobsen, P. (2021). HYPERAKTIV: An activity dataset from adult patients with attention-deficit/hyperactivity disorder (ADHD). En *Proceedings of the 12th ACM Multimedia Systems Conference (MMSys '21)*. Association for Computing Machinery. https://doi.org/10.1145/3458305.3478454

Kessler, R. C., Adler, L., Ames, M., Demler, O., Faraone, S. A., Hiripi, E., Gruber, M. J., Houle, J. J., Merikangas, K. R., Wand, O. M., & Zaslavsky, A. M. (2005). The World Health Organization adult ADHD self-report scale (ASRS): A short screening scale for use in the general population. *Psychological Medicine*, *35*(2), 245–256. https://doi.org/10.1017/S0033291704002892

Ward, M. F., Wender, P. H., & Reimherr, F. W. (1993). The Wender Utah Rating Scale: An aid in the retrospective diagnosis of childhood attention deficit hyperactivity disorder. *The American Journal of Psychiatry*, *150*(6), 885–890. https://doi.org/10.1176/ajp.150.6.885

Zigmond, A. S., & Snaith, R. P. (1983). The Hospital Anxiety and Depression Scale. *Acta Psychiatrica Scandinavica*, *67*(6), 361–370. https://doi.org/10.1111/j.1600-0447.1983.tb09716.x
