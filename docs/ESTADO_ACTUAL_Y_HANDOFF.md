# Estado Actual del Proyecto y Guía de Handoff (Richie $\leftrightarrow$ Mariana)

**Fecha de actualización:** 20 de noviembre de 2026  
**Propósito de este documento:** Proveer contexto completo y verificado del proyecto final de *Análisis de Regresión y Correlación (ARC)* para que Mariana y su agente puedan retomar el trabajo sin pérdida de continuidad.

---

## 1. Resumen Ejecutivo y Fechas Clave

- **Objetivo del proyecto:** Modelar la severidad autorreportada de síntomas de TDAH en adultos (`ASRS`, escala 0–72) en el dataset clínico **HYPERAKTIV** (Hicks et al., 2021) mediante **Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO / OLS)**.
- **Entrega del reporte final (Obsidian Markdown $\rightarrow$ LaTeX/PDF):** **Miércoles 25 de noviembre de 2026 (11:59 p.m.)**.
- **Exposición oral (12–15 min):** **Jueves 26 de noviembre de 2026**.
- **Entorno técnico:** Python 3.13.17 gestionado con `uv` (`uv sync`, `uv run jupyter lab`).

---

## 2. Arquitectura y Convenciones Acordadas

1. **Estructura de 4 notebooks separados por etapa (Opción 2):**
   - `notebooks/01_data_ingestion_and_cleaning.ipynb` — Ingesta, auditoría de calidad e integración.
   - `notebooks/02_eda_and_feature_selection.ipynb` — EDA, correlaciones de Pearson ($r$), gráficas de dispersión y validación de multicolinealidad (VIF).
   - `notebooks/03_ols_modeling_and_diagnostics.ipynb` — Planteamiento MCO, estimación en `statsmodels`, pruebas $F$/$t$, gráfica real vs. predicho y diagnóstico de supuestos de los residuales.
   - `notebooks/04_transformations_and_forecasting.ipynb` — Transformaciones de variables (con reversión a escala original), estimaciones puntuales con intervalos al 95 % para perfiles clínicos y conclusión de utilidad.
2. **Convenciones de código:** Nombres de variables estándar de ciencia de datos en inglés (`TARGET_COL`, `FEATURE_COLS`, `DATA_PATH`, `FIG_DIR`, `TAB_DIR`, `df_model`, `X`, `y`, `X_const`, `ols_model`, `y_pred`, `residuals`, `coef_df`, `metrics_df`, `diagnostics_df`).
3. **Flujo Git:** Trabajo por ramas `feature/*`, *commit* por hito y *merge* a `main`. Antes de trabajar, ejecutar siempre `git checkout main && git pull origin main` y crear una rama nueva.

---

## 3. Qué Ya Está Completado (Resultados Verificados)

### Notebook 01: `notebooks/01_data_ingestion_and_cleaning.ipynb` — COMPLETADO
- Integró los 3 CSV crudos (`patient_info.csv`, `features.csv`, `CPT_II_ConnersContinuousPerformanceTest.csv`, todos con `sep=";"` y `encoding="utf-8-sig"` en CPT-II).
- Filtró sesiones inválidas de CPT-II (`Raw Score Omissions < 300`), descartó filas sin `ASRS` y eliminó columnas de detalle por ensayo.
- **Salida oficial:** `data/processed/hyperaktiv_arc_clean.csv` (**75 pacientes × 885 columnas**; `ASRS`: media `41.39`, DE `13.90`, rango `6.0–68.0`).

### Notebook 02: `notebooks/02_eda_and_feature_selection.ipynb` — COMPLETADO
- **EDA de `ASRS` (Mariana):** Distribución aproximadamente simétrica (media ≈ 41.4, mediana = 42, sin atípicos en boxplot). Figura: `reports/figures/asrs_distribucion.png`.
- **Correlaciones de Pearson $r$ (Mariana — Rúbrica 1b):** Se excluyeron `ID`, variables binarias y diagnósticos directos (`ADHD`, `ADD`) para evitar fuga de datos. Tabla oficial: `reports/tables/correlaciones_asrs.csv`.
- **Dispersión con línea de tendencia (Mariana — Rúbrica 1a):** Figura: `reports/figures/dispersion_candidatas.png`. Se descartó `Omissions` por un punto influyente ($\approx 330$) y `DPrime` por alta colinealidad con `Commissions` ($r = 0.88$).
- **Validación de multicolinealidad VIF (Richie):**
  - Predictores confirmados (`FEATURE_COLS`): `["WURS", "General TScore Commissions", "HADS_A"]`.
  - **Muestra efectiva sin nulos:** **$n_{\text{efectivo}} = 69 \ge 30$** (1 nulo en `WURS`, 6 en `HADS_A`, 0 en `ASRS` y `Commissions`).
  - **Valores VIF (todos $< 2$, umbral $< 5$):**
    - `WURS`: **1.623**
    - `General TScore Commissions`: **1.390**
    - `HADS_A`: **1.205**
  - Tabla oficial: `reports/tables/ols_vif.csv`.

### Notebook 03: `notebooks/03_ols_modeling_and_diagnostics.ipynb` — COMPLETADO
*(En proceso de merge desde `feature/nb03-ols-modeling` hacia `main`).*

- **Ecuación estimada MCO ($n = 69$ — Rúbrica 2a):**
  $$\widehat{\text{ASRS}}_i = 7.6350 + 0.3678\,\text{WURS}_i + 0.3079\,\text{Commissions}_i + 0.1273\,\text{HADS\_A}_i$$
- **Tabla de coeficientes (`reports/tables/ols_coefficients.csv` — Rúbrica 2b y 4b):**

| Término | Coeficiente ($\hat{\beta}$) | Error Estándar | $t$ | $p$-valor | IC 95 % |
|---|---:|---:|---:|---:|---|
| `const` | `7.6350` | `6.1095` | `1.2497` | `0.2159` | `[-4.5666, 19.8365]` |
| `WURS` | `0.3678` | `0.0736` | `4.9957` | `< 0.0001` | `[0.2208, 0.5149]` |
| `General TScore Commissions` | `0.3079` | `0.1162` | `2.6507` | `0.0101` | `[0.0759, 0.5399]` |
| `HADS_A` | `0.1273` | `0.2833` | `0.4492` | `0.6547` | `[-0.4385, 0.6931]` |

- **Métricas globales (`reports/tables/ols_summary_metrics.csv` — Rúbrica 4a y 4b):**
  - $n = 69$
  - **$R^2 = 0.5341$** | **$R^2_{\text{ajustado}} = 0.5126$**
  - **$F(3, 65) = 24.8355$** ($p = 8.00 \times 10^{-11} < 0.001$)
  - $\text{RMSE} = 9.9015$ | $\text{AIC} = 516.08$ | $\text{BIC} = 525.02$
- **Hallazgo clínico clave:** Aunque `HADS_A` tenía correlación bivariada significativa con `ASRS` ($r = 0.304$), al controlar por `WURS` (síntomas en la infancia, con la que correlaciona $r = 0.41$) y `Commissions`, `HADS_A` deja de ser estadísticamente significativa ($p = 0.6547$).
- **Evaluación visual real vs. predicho (Rúbrica 4c):** `reports/figures/ols_real_vs_predicho.png`.
- **Diagnóstico de supuestos de residuales (`reports/tables/ols_diagnostics.csv` y `reports/figures/ols_residual_diagnostics.png`):**
  - **Normalidad (Shapiro-Wilk):** $W = 0.9780$, $p = 0.2634 > 0.05$ (cumple normalidad; Omnibus $p = 0.885$, Jarque-Bera $p = 0.991$).
  - **Homocedasticidad (Breusch-Pagan):** $\text{LM} = 6.7705$, $p = 0.0796 > 0.05$ ($F = 2.3573, p = 0.0798$; cumple al $\alpha = 0.05$, aunque $p \approx 0.08$ justifica explorar transformaciones en el Notebook 04).
  - **Independencia (Durbin-Watson):** $\text{DW} = 2.174$ (sin autocorrelación).
  - **Puntos influyentes (Distancia de Cook):** 5 observaciones con $D_i > 4/n$ (`0.0580`), **0 observaciones con $D_i > 1.0$** (modelo estable).

---

## 4. Mapa de Cumplimiento de la Rúbrica

| Elemento de la Rúbrica | Estado | Dónde está |
|---|---|---|
| **1a.** Gráficas de dispersión | Completado | Notebook 02 (`dispersion_candidatas.png`) |
| **1b.** Coeficiente de correlación de Pearson ($r$) e interpretación | Completado | Notebook 02 (`correlaciones_asrs.csv`) |
| **2a.** Planteamiento formal de la ecuación MCO | Completado | Notebook 03 |
| **2b.** Interpretación teórica y práctica de $\hat{\beta}_0, \hat{\beta}_j$ | Completado (revisable por Mariana para matices clínicos) | Notebook 03 (`ols_coefficients.csv`) |
| **3a.** Transformaciones de variables + reversión a escala original | **PENDIENTE** | Notebook 04 |
| **4a.** $R^2$ y $R^2_{\text{ajustado}}$ | Completado | Notebook 03 (`ols_summary_metrics.csv`) |
| **4b.** Pruebas de significancia ($F$ global y $t$ individuales) | Completado | Notebook 03 |
| **4c.** Gráfica modelo de regresión vs. datos reales ($y$ vs. $\hat{y}$) | Completado | Notebook 03 (`ols_real_vs_predicho.png`) |
| **5a.** Al menos 2 estimaciones puntuales + conclusión de utilidad | **PENDIENTE** | Notebook 04 |

---

## 5. Qué Falta por Hacer (División de Tareas)

### A. Notebook 04: `notebooks/04_transformations_and_forecasting.ipynb` (Rama `feature/nb04-transformations-forecasting`)

1. **Bloque de Transformaciones y Comparación de Modelos — Rúbrica 3a (`[Líder: Richie | Apoyo: Mariana]`):**
   - **Richie:** Probar y comparar frente al modelo base ($R^2_{\text{adj}} = 0.5126$, Breusch-Pagan $p = 0.0796$, Shapiro-Wilk $p = 0.2634$):
     - Transformación en $Y$: $\ln(\text{ASRS})$ y/o $\sqrt{\text{ASRS}}$, con **reversión explícita a la escala original** (incluyendo corrección de sesgo si aplica, p. ej. factor de Duan o $\exp(\hat{z} + \hat{\sigma}^2/2)$) y RMSE comparable en escala `ASRS`.
     - Opcionalmente: modelo parsimonioso sin `HADS_A` (`WURS` + `General TScore Commissions`, que podría aumentar $R^2_{\text{adj}}$ y mejorar AIC/BIC) para decidir cuál es el **modelo final** para pronósticos.
   - **Mariana:** Documentar la justificación clínica/gráfica de la transformación (o de conservar el modelo lineal base si las transformaciones no mejoran el ajuste) y redactar la explicación de la fórmula de reversión a la escala original de `ASRS`.

2. **Bloque de Estimaciones Puntuales y Pronósticos — Rúbrica 5a (`[Líder: Mariana | Apoyo: Richie]`):**
   - **Mariana (prioritario para desbloquear el cálculo):** Definir **al menos 2 perfiles clínicos de pacientes** (idealmente 3: carga baja, moderada y alta) con valores realistas **dentro del rango observado** en los 69 pacientes para `WURS`, `General TScore Commissions` y `HADS_A` (evitando extrapolación inválida).
   - **Richie:** Calcular con `.get_prediction()` las estimaciones puntuales $\widehat{\text{ASRS}}$, el **intervalo de confianza al 95 %** para la media y el **intervalo de predicción al 95 %** para un paciente individual (y la reversión si se usa modelo transformado), exportando `reports/tables/ols_forecasts.csv` y una gráfica opcional de perfiles.
   - **Mariana:** Redactar la **conclusión de utilidad clínica**: qué tan precisas son las estimaciones (considerando $\text{RMSE} \approx 9.9$ puntos en una escala 0–72), qué aporta el modelo en contexto clínico (cribado/apoyo diagnóstico) y cuáles son sus limitaciones ($n = 69$, autorreporte en `ASRS`/`WURS`, varianza no explicada del $\approx 47 \%$).

### B. Reporte Final en PDF (`reports/reporte_final/`, entrega 25 nov) y Exposición Oral (26 nov)

- **Mariana:**
  - Redacción en Obsidian Markdown de: Introducción y planteamiento del problema (justificación de regresión múltiple vs. series de tiempo), descripción clínica de `ASRS` y variables, EDA y correlaciones ($r$), interpretación práctica/clínica, perfiles de pronóstico y conclusiones generales.
  - Ensamblaje editorial final: Obsidian Markdown $\rightarrow$ LaTeX/PDF (verificando ecuaciones, tablas y figuras) antes del **miércoles 25 de noviembre (11:59 p.m.)**.
  - Exposición oral: Minutos 1–7.
- **Richie:**
  - Redacción técnica/matemática: limpieza e integración ($n$ final), selección por VIF, desarrollo matemático del modelo MCO, tablas de coeficientes/métricas ($R^2, R^2_{\text{adj}}, F, t$), diagnóstico de residuales, transformaciones y cálculos de pronósticos.
  - Exposición oral: Minutos 7–14.

---

## 6. Notas Importantes para el Agente de Mariana

1. **Archivo antiguo a ignorar:** En `reports/tables/` existe `top_correlations_asrs.csv` (del prototipo inicial del 16 de noviembre). **No usarlo en el reporte final**; la tabla oficial de correlaciones es `reports/tables/correlaciones_asrs.csv`.
2. **Tablas y figuras oficiales vigentes para el reporte:**
   - Figuras: `asrs_distribucion.png`, `dispersion_candidatas.png`, `ols_real_vs_predicho.png`, `ols_residual_diagnostics.png`.
   - Tablas: `correlaciones_asrs.csv`, `ols_vif.csv`, `ols_coefficients.csv`, `ols_summary_metrics.csv`, `ols_diagnostics.csv` (y próximamente `ols_transformations_comparison.csv` y `ols_forecasts.csv` del Notebook 04).
3. **Qué puede hacer Mariana de inmediato tras hacer `git pull` de `main`:**
   - Revisar la sección `### 3.3` de `notebooks/03_ols_modeling_and_diagnostics.ipynb` por si desea enriquecer algún matiz clínico.
   - Definir los **2–3 perfiles clínicos de pacientes** para el Notebook 04 (verificando los percentiles / rangos observados de `WURS`, `General TScore Commissions` y `HADS_A` en `hyperaktiv_arc_clean.csv`).
   - Avanzar en el borrador de sus secciones del reporte final en `reports/reporte_final/`.

