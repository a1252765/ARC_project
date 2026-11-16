# Rúbrica Oficial y Acuerdos de Trabajo — Proyecto Final ARC

Este documento resume los lineamientos de la profesora y los acuerdos definidos para el desarrollo del proyecto en `/home/richie/Documents/GitHub/ARC_project`.

## 1. Lineamientos y Rúbrica de la Profesora

* **Equipo:** 2 a 4 integrantes (**Richie y Mariana**).
* **Enfoque elegido:** **Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO)** (justificado por la estructura transversal del dataset HYPERAKTIV; mínimo $n = 30$ observaciones y al menos 2 variables independientes).
* **Elementos obligatorios del análisis:**
  1. **Análisis gráfico y de correlación:**
     * a. Gráficas de dispersión ($X_i$ vs. `ASRS`).
     * b. Cálculo e interpretación del coeficiente de correlación ($r$) entre las variables.
  2. **Construcción del modelo por MCO:**
     * a. Planteamiento formal de la ecuación del modelo y cálculo de los parámetros.
     * b. Interpretación teórica y práctica de cada parámetro de regresión en el contexto del problema.
  3. **Transformaciones (si aplica):**
     * a. Si se detectan relaciones no lineales o varianza creciente en el análisis gráfico, aplicar transformaciones adecuadas (logarítmicas, de potencia, etc.) y **mostrar la reversión de la transformación en los pronósticos**.
  4. **Evaluación del modelo:**
     * a. Cálculo e interpretación de $R^2$ y $R^2_{\text{ajustado}}$ para evaluar el porcentaje de variación explicado.
     * b. Pruebas de hipótesis para coeficientes de regresión ($F$ global y $t$ individuales).
     * c. Gráfica del modelo de regresión vs. datos reales (`ASRS` real vs. $\widehat{\text{ASRS}}$).
  5. **Estimaciones y pronósticos:**
     * a. Realizar al menos **dos estimaciones puntuales** con el modelo obtenido y redactar una conclusión sobre la utilidad de los resultados.
* **Entregables:**
  * **Reporte en PDF:** Planteamiento, justificación del modelo, desarrollo matemático, tablas de resultados, gráficas y conclusiones (no se evalúa el código). Entrega: **miércoles 25 de noviembre a las 11:59 p.m.** en Classroom.
  * **Exposición oral (12–15 min):** Problema, justificación, gráficas, pronósticos e interpretación. Fecha: **jueves 26 de noviembre**.

---

## 2. Acuerdos de Trabajo y Metodología

* **Rol del asistente (IA):** Actuar como **guía y facilitador** paso a paso mediante un checklist por fases, ayudando a Richie y Mariana a aprender y construir el proyecto desde cero. Solo implementa código o tareas directamente cuando se le pida de forma explícita.
* **Entorno de trabajo:**
  * Construir el análisis paso a paso en **Jupyter Notebooks** (`notebooks/01_eda_y_seleccion.ipynb`, `02_modelo_mco_y_evaluacion.ipynb`, `03_transformaciones_y_pronosticos.ipynb`) en una rama nueva (`feature/analisis-desde-cero`), usando `uv` (`uv run jupyter lab`).
* **Criterio de selección de variables (3–4 predictores):**
  * **Enfoque híbrido:** combinar sentido clínico/teórico respecto a `ASRS`, correlación lineal clara ($r$) y ausencia de multicolinealidad ($\text{VIF} < 5$).
* **Reporte y distribución de carga:**
  * Redacción en **Obsidian Markdown $\rightarrow$ LaTeX/PDF**.
  * Reparto equitativo entre Richie y Mariana por fase (detallado en [README.md](../README.md)).

---

## 3. Estado Actual al Cambiar de Workspace

* Repositorio sincronizado en `main` (`a3c72b1`), limpio y con `uv` verificado.
* Datos crudos ya disponibles en `data/raw/` (`patient_info.csv`, `features.csv`, `CPT_II_ConnersContinuousPerformanceTest.csv`) y dataset integrado en `data/processed/hyperaktiv_arc_clean.csv`.
* **Pendiente para iniciar (Fase 0):** crear la rama `feature/analisis-desde-cero` en `/home/richie/Documents/GitHub/ARC_project`, crear `notebooks/01_eda_y_seleccion.ipynb` y arrancar la **Fase 1** en Jupyter Lab.

