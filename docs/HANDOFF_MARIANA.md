# Handoff de Mariana → Richie (actualización)

**Fecha de actualización:** 22 de noviembre de 2026
**Rama de trabajo:** `feature/nb04-transformations-forecasting`
**Propósito:** Informar a Richie y a su agente qué avanzó Mariana desde el handoff del 20 de noviembre (`docs/ESTADO_ACTUAL_Y_HANDOFF.md`) y qué queda pendiente para la entrega del **miércoles 25 de noviembre (11:59 p.m.)**.

---

## 1. Qué completó Mariana

### 1.1 Perfiles clínicos para el Notebook 04 (Rúbrica 5a) — COMPLETADO

- **Archivo:** `notebooks/04_transformations_and_forecasting.ipynb` (commit `52073aa`).
- **Nota:** el notebook venía vacío (0 bytes) y Jupyter no podía abrirlo (`NotJSONError`). Se inicializó como notebook válido.
- **Método:** percentiles 10, 50 y 90 de cada predictor en la muestra efectiva ($n = 69$, casos completos de `FEATURE_COLS` + `ASRS`), redondeados a enteros. Todos los valores están dentro del rango observado (sin extrapolación).
- **Estadísticos de referencia ($n = 69$):**

| Variable | Mín | P10 | P25 | P50 | P75 | P90 | Máx |
|---|---:|---:|---:|---:|---:|---:|---:|
| `WURS` | 5.0 | 16.0 | 26.0 | 38.0 | 57.0 | 65.2 | 88.0 |
| `General TScore Commissions` | 32.9 | 42.8 | 49.6 | 57.3 | 65.9 | 73.3 | 86.9 |
| `HADS_A` | 0.0 | 2.8 | 6.0 | 9.0 | 12.0 | 16.0 | 20.0 |

- **Perfiles definidos** (variable `profiles_df` en el Notebook 04, lista para `.get_prediction()`):

| `perfil` | `WURS` | `General TScore Commissions` | `HADS_A` | Descripción clínica |
|---|---:|---:|---:|---|
| Carga baja (P10) | 16 | 43 | 3 | Pocos síntomas infantiles, impulsividad en el promedio, ansiedad normal (HADS_A 0–7) |
| Carga moderada (P50) | 38 | 57 | 9 | Síntomas infantiles intermedios, impulsividad en el límite alto del promedio, ansiedad limítrofe (8–10) |
| Carga alta (P90) | 65 | 73 | 16 | WURS ≥ 46 (punto de corte de TDAH infantil), impulsividad elevada (T > 60), ansiedad clínica (≥ 11) |

- **Referencia rápida con el modelo base** (los valores oficiales con intervalos los genera `.get_prediction()`): $\widehat{\text{ASRS}} \approx 27.1$ (baja), $40.3$ (moderada) y $56.1$ (alta).

```python
profiles_df = pd.DataFrame({
    "perfil": ["Carga baja", "Carga moderada", "Carga alta"],
    "WURS": [16, 38, 65],
    "General TScore Commissions": [43, 57, 73],
    "HADS_A": [3, 9, 16],
})
```

### 1.2 Borrador de secciones del reporte — COMPLETADO (borrador)

- **Archivo:** `reports/reporte_final/secciones_mariana.md` (commits `f80f234` y `5c281d0`).
- **Contenido (Obsidian Markdown, figuras enlazadas con rutas relativas `../figures/`):**
  1. Introducción y planteamiento del problema (pregunta de investigación y objetivos).
  2. Justificación de regresión lineal múltiple vs. series de tiempo (datos de corte transversal, $n = 69 \ge 30$, $DW = 2.174$).
     - 2.1 Metodología CRISP-ML(Q) con tabla fase → notebook.
  3. Descripción clínica de ASRS y de los predictores (WURS, CPT-II Commissions, HADS_A), con escalas y puntos de corte.
  4. EDA: distribución de ASRS, tabla de correlaciones de Pearson, interpretación de dispersiones (incluye el descarte de Omissions y DPrime) y selección con VIF.
  5. Interpretación clínica de $\hat{\beta}_0, \hat{\beta}_j$, $R^2$ y prueba $F$.
  6. Referencias (Hicks 2021, Kessler 2005, Ward 1993, Zigmond & Snaith 1983, Conners 2000).
- **Pendiente en el borrador:** transformaciones, pronósticos de perfiles, conclusión de utilidad clínica y conclusiones generales (dependen del Notebook 04).

### 1.3 Revisión de la sección 3.3 del Notebook 03 — COMPLETADO

- La interpretación de Richie es correcta y completa; **no se modificó el notebook 03**.
- **Matiz agregado solo en el reporte (sección 5 de Mariana):** comparación del efecto de un aumento de **1 desviación estándar muestral** de cada predictor sobre ASRS, para comparar su peso práctico:
  - `WURS`: DE ≈ 20.8 → $0.3678 \times 20.8 \approx$ **+7.7** puntos de ASRS
  - `General TScore Commissions`: DE ≈ 12.2 → $0.3079 \times 12.2 \approx$ **+3.8**
  - `HADS_A`: DE ≈ 4.7 → $0.1273 \times 4.7 \approx$ **+0.6**
  - Conclusión: WURS pesa aproximadamente el doble que Commissions; HADS_A prácticamente no aporta al controlar por las otras dos.

---

## 2. Qué falta (pendiente de acordar quién hace los cálculos)

### Notebook 04

1. **Transformaciones (Rúbrica 3a):** comparar el modelo base ($R^2_{adj} = 0.5126$, BP $p = 0.0796$, SW $p = 0.2634$) contra $\ln(\text{ASRS})$ y $\sqrt{\text{ASRS}}$ con reversión a escala original y RMSE comparable; opcionalmente modelo sin `HADS_A`. Exportar `reports/tables/ols_transformations_comparison.csv`.
2. **Pronósticos (Rúbrica 5a):** `.get_prediction(...).summary_frame(alpha=0.05)` sobre `profiles_df` con el modelo final (IC 95 % de la media e intervalo de predicción 95 %). Exportar `reports/tables/ols_forecasts.csv`.

**Pregunta abierta para Richie:** ¿los cálculos de 1 y 2 los hace Richie (según el handoff del 20 nov) o Mariana?

### Redacción (Mariana)

- Justificación de transformar o conservar el modelo base y fórmula de reversión.
- Pronósticos de perfiles y conclusión de utilidad clínica (RMSE ≈ 9.9, uso como cribado, limitaciones: $n = 69$, autorreporte, ≈ 47 % de varianza no explicada).
- Conclusiones generales.
- Ensamblaje final Obsidian Markdown → LaTeX/PDF.

### Redacción (Richie)

- Secciones técnicas: limpieza e integración, VIF, desarrollo matemático MCO, tablas de coeficientes y métricas, diagnóstico de residuales, transformaciones y cálculo de pronósticos.

---

## 3. Notas para el agente de Richie

1. **Notebook 03 sin cambios:** los cambios locales de 01, 02 y 03 producidos al abrirlos en Jupyter se descartaron con `git restore`; no se subieron.
2. **Documento desactualizado:** en `docs/METODOLOGIA_CRISP_ML.md`, la fila de la Fase 4 todavía marca como pendientes la gráfica real vs. predicho (4c) y el diagnóstico de residuales, pero ya están completos en el Notebook 03.
3. **Coordinación:** para evitar conflictos en `.ipynb`, avisar antes de editar el Notebook 04 y hacer `git pull` antes de empezar.

---

## 4. Respuesta y cierre de Richie (25 de noviembre de 2026)

**Todo el análisis (Notebooks 01–04) y las secciones técnicas de Richie están 100 % completados y listos en `main`:**

1. **Notebook 04 completado y ejecutado (`notebooks/04_transformations_and_forecasting.ipynb`):**
   - **Transformaciones (Rúbrica 3a):** se comparó el modelo base contra $\ln(\text{ASRS})$, $\sqrt{\text{ASRS}}$ (con reversión analítica a escala original) y el modelo parsimonioso sin `HADS_A`. Tabla oficial en `reports/tables/ols_transformations_comparison.csv`. Se conserva el **modelo lineal base (3 predictores)** al ser el único que cumple simultáneamente normalidad (Shapiro-Wilk $p = 0.2634$) y homocedasticidad (Breusch-Pagan $p = 0.0796$) y obtiene el menor RMSE en escala `ASRS` (`9.6102`).
   - **Pronósticos clínicos (Rúbrica 5a):** calculados sobre `profiles_df` con `.get_prediction().summary_frame(alpha=0.05)` $\rightarrow$ `reports/tables/ols_forecasts.csv` y `reports/figures/ols_forecasts_profiles.png` (`Carga baja: 27.14`, `Carga moderada: 40.31`, `Carga alta: 56.06`).
2. **Secciones técnicas de Richie listas:** `reports/reporte_final/secciones_richie.md` (en Obsidian Markdown, listas para fusionarse con `reports/reporte_final/secciones_mariana.md`).
3. **Metodología actualizada:** `docs/METODOLOGIA_CRISP_ML.md` actualizado con Fases 1–5 completadas.
4. **Siguiente paso único para Mariana (entrega hoy 25 nov, 11:59 p.m.):** cerrar los párrafos de utilidad clínica/conclusiones generales en `secciones_mariana.md`, integrar `secciones_richie.md` y exportar el **PDF final** (Obsidian Markdown $\rightarrow$ LaTeX/PDF).
