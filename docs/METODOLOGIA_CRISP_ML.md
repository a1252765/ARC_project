# Metodología CRISP-ML(Q) / CRISP-DM y Estado de Avance del Proyecto

**Proyecto:** Modelado de la Severidad de Síntomas de TDAH en Adultos (`ASRS`) mediante Regresión Lineal Múltiple (MCO / OLS)  
**Dataset:** HYPERAKTIV (Hicks et al., 2021)  
**Equipo:** Richie & Mariana  
**Última actualización:** 25 de noviembre de 2026

---

## 1. Visión General del Marco Metodológico

El desarrollo del proyecto sigue el estándar de ciencia de datos **CRISP-DM / CRISP-ML(Q)** (*Cross-Industry Standard Process for Machine Learning with Quality Assurance*), estructurando el flujo de trabajo en **6 fases iterativas** con controles de calidad explícitos (reproducibilidad, prevención de fuga de datos, validación estadística de supuestos y trazabilidad en Git).

| Fase CRISP-ML(Q) | Notebook / Entregable Principal | Rúbrica ARC Cubierta | Estado Actual |
| :--- | :--- | :--- | :--- |
| **1. Comprensión del Negocio y de los Datos** (*Business & Data Understanding*) | `docs/` y `notebooks/01_data_ingestion_and_cleaning.ipynb`, `02_eda_and_feature_selection.ipynb` | 1a, 1b | **Completado** |
| **2. Preparación de los Datos** (*Data Preparation*) | `notebooks/01_data_ingestion_and_cleaning.ipynb`, `02_eda_and_feature_selection.ipynb` | 1a, 1b | **Completado** |
| **3. Modelado** (*Modeling*) | `notebooks/03_ols_modeling_and_diagnostics.ipynb` (Secciones 1–3) | 2a, 2b | **Completado** |
| **4. Evaluación y Aseguramiento de Calidad** (*Evaluation & QA*) | `notebooks/03_ols_modeling_and_diagnostics.ipynb` (Secciones 3–5) y `04_transformations_and_forecasting.ipynb` (Sección 2) | 3a, 4a, 4b, 4c | **Completado** |
| **5. Despliegue / Inferencia Aplicada** (*Deployment / Forecasting*) | `notebooks/04_transformations_and_forecasting.ipynb` (Sección 3) | 5a | **Completado** |
| **6. Comunicación y Monitoreo / Reporte Final** (*Documentation & Reporting*) | `reports/reporte_final/` (`secciones_mariana.md`, `secciones_richie.md` $\rightarrow$ PDF) y presentación oral | Todas | **En progreso** (secciones listas; falta ensamblaje PDF) |

---

## 2. Trabajo Realizado por Fase de CRISP-ML(Q)

### Fase 1: Comprensión del Problema Clínico y de los Datos (*Business & Data Understanding*)

#### Objetivo metodológico
Definir el problema clínico a resolver, la variable objetivo ($Y$), las fuentes de datos disponibles y explorar la estructura y distribución estadística de las variables antes de modelar.

#### Trabajo realizado
1. **Formulación del problema clínico y estadístico:**
   - **Variable respuesta ($Y$):** `ASRS` (*Adult ADHD Self-Report Scale*, escala continua de 0 a 72 puntos que cuantifica la severidad actual de síntomas de TDAH en adultos).
   - **Enfoque analítico:** Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO / OLS) sobre datos de corte transversal ($n \ge 30$, al menos 2 variables predictoras $X_j$).
2. **Auditoría de fuentes crudas (`notebooks/01_data_ingestion_and_cleaning.ipynb`):**
   - Inspección de las 3 tablas originales del estudio clínico HYPERAKTIV en `data/raw/`:
     - `patient_info.csv`: datos demográficos, diagnósticos clínicos y escalas psicométricas (`ASRS`, `WURS`, `MADRS`, `HADS_A`, `HADS_D`).
     - `features.csv`: características extraídas de series de actigrafía motora (`ACC__*`).
     - `CPT_II_ConnersContinuousPerformanceTest.csv`: métricas neuropsicológicas objetivas de atención sostenida e inhibición motora (`TScore Commissions`, `DPrime`, `Omissions`, `HitRT`, `VarSE`, etc.).
   - Identificación de formato (`sep=";"`) y codificación (`utf-8-sig` en CPT-II), tipos de datos y conteo de valores faltantes.
3. **Análisis Exploratorio de Datos — EDA (`notebooks/02_eda_and_feature_selection.ipynb`):**
   - **Distribución de `ASRS`:** histograma y diagrama de caja exportados en `reports/figures/asrs_distribucion.png` ($n = 75$, media $= 41.39$, mediana $= 42.0$, desviación estándar $= 13.90$, rango de $6.0$ a $68.0$). Se verificó simetría aproximada y ausencia de valores atípicos extremos que obligaran a transformar $Y$ a priori.
   - **Análisis de correlación lineal (Rúbrica 1b):** cálculo de correlaciones de Pearson ($r$) y $p$-valores frente a `ASRS`, exportado en `reports/tables/correlaciones_asrs.csv`.
   - **Análisis gráfico bivariado (Rúbrica 1a):** panel de gráficas de dispersión ($X_j$ vs. `ASRS`) con recta de tendencia ajustada en `reports/figures/dispersion_candidatas.png` para evaluar linealidad, dispersión y posibles puntos influyentes (detectando que la correlación de `General TScore Omissions` estaba distorsionada por un valor extremo $\approx 330$).

---

### Fase 2: Preparación de los Datos (*Data Preparation*)

#### Objetivo metodológico
Integrar las fuentes de datos, aplicar reglas de limpieza y control de calidad (QA), prevenir fuga de información (*data leakage*) y seleccionar el subconjunto óptimo de predictores ($X$) libre de multicolinealidad.

#### Trabajo realizado
1. **Limpieza e integración por `ID` (`notebooks/01_data_ingestion_and_cleaning.ipynb`):**
   - Verificación de unicidad de `ID` y cruce relacional (*inner join*) entre `patient_info`, `features` y `CPT_II`.
   - Eliminación de columnas de detalle ensayo por ensayo del CPT-II para conservar únicamente variables agregadas clínicamente interpretables.
   - Filtrado de observaciones con variable objetivo `ASRS` válida, generando el dataset maestro limpio en `data/processed/hyperaktiv_arc_clean.csv` (`75 filas × 885 columnas`).
2. **Prevención de fuga de datos (*Data Leakage*) y filtrado de candidatas (`notebooks/02_eda_and_feature_selection.ipynb`):**
   - Exclusión explícita de identificadores (`ID`) y de etiquetas diagnósticas directas (`ADHD`, `ADD`) que representan el resultado diagnóstico mismo.
3. **Selección híbrida de características (*Feature Selection*) y control de multicolinealidad (`notebooks/02_eda_and_feature_selection.ipynb`):**
   - Inspección de la matriz de correlación entre candidatas: se detectó alta colinealidad entre `General TScore Commissions` y `General TScore DPrime` ($r = 0.88$), conservando `Commissions` por su mayor correlación con `ASRS` ($r = 0.526$ vs. $0.398$) y su interpretación clínica directa como impulsividad motora.
   - Definición de los **3 predictores complementarios** (`FEATURE_COLS`) y depuración de valores faltantes (`n_effective = 69` casos completos $\ge 30$):
     1. `WURS` ($r = 0.685, p < 0.0001$): carga retrospectiva de síntomas de TDAH en la infancia.
     2. `General TScore Commissions` ($r = 0.526, p < 0.0001$): errores de comisión (impulsividad objetiva en el CPT-II).
     3. `HADS_A` ($r = 0.304, p = 0.0111$): sintomatología de ansiedad comórbida.
   - **Validación formal por Factor de Inflación de Varianza (VIF):** cálculo con constante en `statsmodels`, exportado a `reports/tables/ols_vif.csv`. Todos los valores cumplieron holgadamente el criterio $\text{VIF} < 5$ (e incluso $< 2$):
     - `WURS`: $\text{VIF} = 1.623$
     - `General TScore Commissions`: $\text{VIF} = 1.390$
     - `HADS_A`: $\text{VIF} = 1.205$

---

### Fase 3: Modelado (*Modeling*)

#### Objetivo metodológico
Especificar matemáticamente el modelo de Regresión Lineal Múltiple y estimar sus parámetros por Mínimos Cuadrados Ordinarios (MCO / OLS).

#### Trabajo realizado (`notebooks/03_ols_modeling_and_diagnostics.ipynb`, Secciones 1–3)
1. **Planteamiento formal de la ecuación (Rúbrica 2a):**
   - Especificación de la ecuación poblacional y estimada, junto con la tabla de unidades y escalas clínicas:
     $$\text{ASRS}_i = \beta_0 + \beta_1\,\text{WURS}_i + \beta_2\,\text{Commissions}_i + \beta_3\,\text{HADS\_A}_i + \varepsilon_i$$
2. **Estimación por MCO en `statsmodels` (`n_obs = 69`):**
   - Ecuación estimada resultante:
     $$\widehat{\text{ASRS}}_i = 7.6350 + 0.3678\,\text{WURS}_i + 0.3079\,\text{Commissions}_i + 0.1273\,\text{HADS\_A}_i$$
   - Exportación de coeficientes, errores estándar, estadísticos $t$, $p$-valores e intervalos de confianza al 95 % en `reports/tables/ols_coefficients.csv`.
3. **Interpretación teórica y clínica *ceteris paribus* (Rúbrica 2b):**
   - Documentación detallada del significado matemático del intercepto ($\hat{\beta}_0 = 7.6350, p = 0.2159$) y del efecto marginal de cada predictor manteniendo constantes los demás ($\hat{\beta}_1 = 0.3678$ puntos de `ASRS` por punto en `WURS`; $\hat{\beta}_2 = 0.3079$ puntos de `ASRS` por punto $T$ en `Commissions`; y dilución del efecto directo de `HADS_A`, $\hat{\beta}_3 = 0.1273, p = 0.6547$, al controlar por `WURS`).

---

### Fase 4: Evaluación y Aseguramiento de Calidad (*Evaluation & Quality Assurance*)

#### Objetivo metodológico
Evaluar la bondad de ajuste y significancia estadística del modelo, contrastar visualmente las predicciones contra los valores reales, verificar el cumplimiento de los supuestos clásicos de Gauss-Markov sobre los residuales y determinar si se requieren transformaciones funcionales.

#### Trabajo realizado hasta el momento (`notebooks/03_ols_modeling_and_diagnostics.ipynb`, Sección 3)
1. **Métricas de bondad de ajuste exportadas en `reports/tables/ols_summary_metrics.csv` (Rúbrica 4a):**
   - $R^2 = 0.5341$ (el modelo explica el **53.41 %** de la varianza de `ASRS`).
   - $R^2_{\text{ajustado}} = 0.5126$ (**51.26 %** penalizado por $k = 3$ predictores).
   - $\text{RMSE} = 9.9015$ puntos en la escala `ASRS` (0–72), $\text{AIC} = 516.08$, $\text{BIC} = 525.02$.
2. **Pruebas de significancia global e individual (Rúbrica 4b):**
   - **Prueba $F$ global:** $F(3, 65) = 24.8355$, $p = 8.00 \times 10^{-11} < 0.001$ (rechazo contundente de $H_0: \beta_1 = \beta_2 = \beta_3 = 0$).
   - **Pruebas $t$ individuales ($\alpha = 0.05$):** `WURS` ($t = 4.9957, p < 0.0001$) y `General TScore Commissions` ($t = 2.6507, p = 0.0101$) resultan estadísticamente significativos; `HADS_A` ($t = 0.4492, p = 0.6547$) no resulta significativo.

#### Trabajo completado adicional en esta fase (`notebooks/03_ols_modeling_and_diagnostics.ipynb` y `04_transformations_and_forecasting.ipynb`)
- **Gráfica de valores reales vs. predichos (Rúbrica 4c):** dispersión de $y$ vs. $\hat{y}$ con línea identidad ($y = x$) en `reports/figures/ols_real_vs_predicho.png`.
- **Diagnóstico gráfico y formal de residuales:** panel $2 \times 2$ en `reports/figures/ols_residual_diagnostics.png` y pruebas en `reports/tables/ols_diagnostics.csv` (Shapiro-Wilk $W = 0.9780, p = 0.2634$; Breusch-Pagan $\text{LM} = 6.7705, p = 0.0796$; Durbin-Watson $= 2.174$; 0 observaciones con Cook $> 1.0$).
- **Evaluación de transformaciones y reversión a escala original (Rúbrica 3a):** comparación del modelo base contra $\ln(\text{ASRS})$, $\sqrt{\text{ASRS}}$ (con reversión insesgada) y modelo parsimonioso sin `HADS_A` en `reports/tables/ols_transformations_comparison.csv`. Se conserva el modelo base lineal al ser el único que cumple simultáneamente normalidad y homocedasticidad y logra el menor RMSE en escala `ASRS` (`9.6102`).

---

### Fase 5: Despliegue / Inferencia Aplicada (*Deployment / Forecasting*)

#### Objetivo metodológico
Utilizar el modelo validado para generar estimaciones puntuales e intervalos de confianza/predicción al 95 % sobre perfiles clínicos realistas y evaluar su utilidad práctica en la toma de decisiones clínicas.

#### Trabajo completado (`notebooks/04_transformations_and_forecasting.ipynb`)
- Definición de **3 perfiles clínicos** por percentiles P10, P50 y P90 ($n = 69$, sin extrapolación): Carga baja, Carga moderada y Carga alta.
- Cálculo de pronósticos puntuales ($\widehat{\text{ASRS}} = 27.14$, $40.31$ y $56.06$), IC 95 % de la media e IP 95 % individual con `.get_prediction()` en `reports/tables/ols_forecasts.csv` y gráfica `reports/figures/ols_forecasts_profiles.png` (**Rúbrica 5a**).
- Documentación de la utilidad clínica (estratificación/apoyo al cribado) y limitaciones ($\text{RMSE} \approx 9.9$, $n = 69$, autorreporte).

---

### Fase 6: Comunicación y Reporte Final (*Documentation & Reporting*)

#### Objetivo metodológico
Integrar los hallazgos matemáticos, estadísticos y clínicos en un documento técnico reproducible y preparar la defensa oral del proyecto.

#### Estado actual (`reports/reporte_final/`)
- **Borradores listos:** `reports/reporte_final/secciones_mariana.md` y `reports/reporte_final/secciones_richie.md`.
- **Pendiente (25 nov):** cierre de párrafos finales de Mariana y ensamblaje editorial **Obsidian Markdown $\rightarrow$ LaTeX/PDF** (entrega: **miércoles 25 de noviembre de 2026, 11:59 p.m.**).
- **Exposición oral:** 12–15 minutos (**jueves 26 de noviembre de 2026**).

