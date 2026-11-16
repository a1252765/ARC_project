# Proyecto Final — Análisis de Regresión y Correlación (ARC)

Modelado de la severidad de síntomas de TDAH en adultos (`ASRS`) en el dataset clínico **HYPERAKTIV** (Hicks et al., 2021) mediante **Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO)**.

## Equipo y Roles (Distribución Equitativa)

* **Richie:** Ingeniería de datos, ajuste MCO (`statsmodels`), diagnóstico de residuales/transformaciones, cálculo de pronósticos y secciones técnicas/matemáticas del reporte.
* **Mariana:** Análisis exploratorio gráfico (EDA) y correlaciones, interpretación clínica/práctica de parámetros, definición de perfiles de pronóstico, conclusiones y ensamblaje editorial (Obsidian Markdown $\rightarrow$ LaTeX/PDF).

| Fase | Líder | Apoyo | Balance de carga |
| :--- | :--- | :--- | :--- |
| **Fase 0:** Rama, datos y entorno | **Richie y Mariana** | — | Configuración inicial conjunta |
| **Fase 1:** Integración, EDA y VIF | **Mariana** (EDA y $r$) | **Richie** (carga, limpieza y VIF) | Datos + Gráficas + Selección conjunta |
| **Fase 2:** Modelo MCO y pruebas | **Richie** (ecuación y `statsmodels`) | **Mariana** (interpretación clínica) | Ajuste técnico + Interpretación |
| **Fase 3:** Diagnóstico y transformaciones | **Richie** (residuales y pruebas) | **Mariana** (análisis visual y reversión) | Diagnóstico + Comparación |
| **Fase 4:** Estimaciones y pronósticos | **Mariana** (perfiles y utilidad) | **Richie** (cálculo e intervalos) | Perfiles/conclusión + Cómputo |
| **Fase 5:** Reporte PDF y exposición | **Richie y Mariana** | — | Mitad de secciones y 6–7 min c/u |

## Fechas Clave

* **Jueves 19 de noviembre:** Registro de equipo y base de datos con el profesor.
* **Miércoles 25 de noviembre (11:59 p.m.):** Entrega del reporte final en PDF en Classroom (basta con que un integrante realice la entrega).
* **Jueves 26 de noviembre:** Exposición oral (12–15 min aprox.).

---

## Configuración Inicial en Ubuntu con `uv`

1. **Instalar `uv` (si no está instalado):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   Reinicia la terminal o ejecuta `source ~/.local/bin/env`.
2. **Clonar el repositorio y sincronizar dependencias:**
   ```bash
   git clone <URL_DEL_REPO_EN_GITHUB>
   cd ARC_project
   uv sync
   ```
3. **Colocar los datos crudos en `data/raw/`:**
   * `data/raw/patient_info.csv`
   * `data/raw/features.csv`
   * `data/raw/CPT_II_ConnersContinuousPerformanceTest.csv`
   *(Los `.csv` están en `.gitignore` para no subir el dataset al repositorio).*
4. **Abrir Jupyter para trabajar los notebooks paso a paso:**
   ```bash
   uv run jupyter lab
   ```

---

## Guía Detallada Paso a Paso (De Cero al Reporte Final)

Esta guía sigue los **5 elementos obligatorios de la rúbrica** y está pensada para construirse en **Jupyter Notebooks** dentro de `notebooks/`.

### Fase 0: Rama Limpia, Datos y Estructura — `[Richie y Mariana]`
1. **`[Richie]` Crear una rama nueva desde `main`** para construir el análisis desde cero:
   ```bash
   git checkout main && git pull
   git checkout -b feature/analisis-desde-cero
   ```
2. **`[Richie y Mariana]` Verificar que los 3 CSV existen en su `data/raw/` local** (separador `;` y codificación `utf-8-sig` en el archivo de CPT-II) y confirmar que `uv sync` funciona en ambas computadoras.
3. **`[Richie]` Crear la carpeta `notebooks/`** con tres notebooks base y subir la estructura inicial a la rama:
   * `notebooks/01_eda_y_seleccion.ipynb`
   * `notebooks/02_modelo_mco_y_evaluacion.ipynb`
   * `notebooks/03_transformaciones_y_pronosticos.ipynb`

---

### Fase 1: Integración de Datos, EDA y Selección de Predictores (Rúbrica 1) — `[Líder: Mariana | Apoyo: Richie]`
**Objetivo:** Justificar el enfoque de regresión lineal múltiple ($n \ge 30$, al menos 2 variables independientes), limpiar los datos, analizar gráficas de dispersión y seleccionar 3–4 predictores con sentido clínico y sin multicolinealidad.

1. **`[Richie]` Carga, limpieza e integración por `ID`:**
   * Cargar `patient_info.csv`, `features.csv` y `CPT_II_ConnersContinuousPerformanceTest.csv` (`sep=";"`).
   * Revisar duplicados por `ID`, valores faltantes y tipos de datos.
   * Aplicar regla de calidad en CPT-II: filtrar sesiones inválidas (por ejemplo, `Raw Score Omissions >= 300`, donde el paciente no respondió o se desconectó el teclado).
   * Unir las tablas por `ID` (inner join) y descartar filas sin `ASRS` (variable respuesta $Y$). Verificar que $n \ge 30$.
2. **`[Mariana]` Análisis gráfico inicial (Rúbrica 1a):**
   * Graficar la distribución de `ASRS` (histograma + boxplot) y exportar a `reports/figures/`.
   * Generar **gráficas de dispersión** ($X_i$ vs `ASRS`) con línea de tendencia para las variables candidatas, documentando si la relación parece lineal o curva y si hay varianza creciente (heterocedasticidad) o valores atípicos.
3. **`[Mariana]` Cálculo e interpretación de correlación $r$ (Rúbrica 1b):**
   * Calcular la matriz de correlación de Pearson ($r$) y los $p$-valores respecto a `ASRS`.
   * Excluir identificadores (`ID`) o diagnósticos directos redundantes si generan fuga de información (`ADHD`, `ADD`).
   * Redactar la interpretación de dirección, magnitud y significancia estadística de cada $r$.
4. **`[Richie y Mariana]` Selección híbrida de 3–4 predictores y control de multicolinealidad (VIF):**
   * Elegir en conjunto **3 a 4 variables independientes** ($X_1, X_2, X_3, \dots$) combinando relevancia clínica respecto al TDAH (`ASRS`) y correlación lineal clara.
   * **`[Richie]`** Calcular el **Factor de Inflación de Varianza (VIF)** con `statsmodels.stats.outliers_influence.variance_inflation_factor` y verificar que **$\text{VIF} < 5$** para todos los predictores elegidos; guardar la tabla en `reports/tables/` y el dataset integrado en `data/processed/`.

---

### Fase 2: Construcción del Modelo MCO e Interpretación (Rúbrica 2 y 4a–4b) — `[Líder: Richie | Apoyo: Mariana]`
**Objetivo:** Plantear formalmente el modelo, estimarlo por MCO en `statsmodels`, interpretar cada parámetro y evaluarlo estadísticamente.

1. **`[Richie]` Planteamiento formal de la ecuación (Rúbrica 2a):**
   $$\widehat{\text{ASRS}}_i = \hat{\beta}_0 + \hat{\beta}_1 X_{1i} + \hat{\beta}_2 X_{2i} + \dots + \hat{\beta}_k X_{ki}$$
   Documentar el significado y unidades de $Y$ y de cada $X_j$.
2. **`[Richie]` Ajuste MCO en `statsmodels`:**
   * Añadir constante (`sm.add_constant`) y ajustar `sm.OLS(y, X).fit()`.
   * Extraer la tabla resumen (`.summary()`) y exportar coeficientes/métricas a `reports/tables/`.
3. **`[Mariana]` Interpretación teórica y práctica de parámetros (Rúbrica 2b):**
   * **Intercepto ($\hat{\beta}_0$):** valor esperado de `ASRS` cuando todos los predictores son 0 (indicar si tiene sentido clínico o solo matemático).
   * **Pendientes ($\hat{\beta}_j$):** cambio esperado en `ASRS` por cada incremento de 1 unidad en $X_j$, manteniendo constantes las demás variables (*ceteris paribus*), traducido al contexto clínico del TDAH.
4. **`[Richie y Mariana]` Evaluación global e individual (Rúbrica 4a y 4b):**
   * **`[Richie]`** Reportar $R^2$, $R^2_{\text{ajustado}}$, estadístico $F$ ($H_0: \beta_1 = \dots = \beta_k = 0$), estadísticos $t$ individuales ($H_0: \beta_j = 0$), $p$-valores e IC al 95%.
   * **`[Mariana]`** Redactar la conclusión estadística de qué porcentaje de variación explica el modelo y qué predictores resultan significativos.

---

### Fase 3: Diagnóstico Gráfico, Transformaciones y Comparación (Rúbrica 3a y 4c) — `[Líder: Richie | Apoyo: Mariana]`
**Objetivo:** Verificar si se cumplen los supuestos del modelo lineal, aplicar transformaciones solo si es necesario y graficar valores reales vs. ajustados.

1. **`[Richie]` Diagnóstico de residuales:**
   * Graficar residuales vs. valores ajustados (detectar no linealidad o forma de embudo/varianza creciente).
   * Graficar Q-Q plot / histograma de residuales (normalidad) y revisar puntos influyentes (distancia de Cook).
2. **`[Richie y Mariana]` Transformaciones (Rúbrica 3a — si aplica):**
   * **`[Richie]`** Si las gráficas muestran relación no lineal o varianza creciente, probar transformaciones ($\ln(Y)$, $\sqrt{Y}$, $\ln(X_j)$ o términos polinomiales) y comparar $R^2_{\text{ajustado}}$ y residuales frente al modelo base.
   * **`[Mariana]`** Documentar la justificación gráfica de transformar (o no transformar) y, si se transforma $Y$, redactar la fórmula de **reversión de la transformación** para regresar a la escala original de `ASRS` (por ejemplo, $\hat{Y} = \exp(\widehat{\ln Y})$).
3. **`[Mariana]` Gráfica del modelo de regresión vs. datos reales (Rúbrica 4c):**
   * Generar e interpretar la gráfica de `ASRS` real vs. $\widehat{\text{ASRS}}$ predicho con la línea identidad ($y = x$) y exportarla a `reports/figures/`.

---

### Fase 4: Estimaciones Puntuales y Pronósticos (Rúbrica 5a) — `[Líder: Mariana | Apoyo: Richie]`
**Objetivo:** Realizar al menos dos estimaciones puntuales con el modelo final y evaluar su utilidad práctica.

1. **`[Mariana]` Definir al menos 2 perfiles de pacientes** (dentro del rango observado de los datos para evitar extrapolación inválida): por ejemplo, un perfil con carga sintomática/conductual baja y otro con carga alta.
2. **`[Richie]` Calcular las estimaciones puntuales** en el notebook (junto con sus intervalos de confianza y predicción al 95% usando `.get_prediction()`).
3. **`[Richie]` Si hubo transformación en $Y$**, mostrar explícitamente en código y tabla la reversión a la escala original de `ASRS`.
4. **`[Mariana]` Redactar conclusión de utilidad:** qué tan precisas son las estimaciones, qué aporta el modelo en contexto clínico y cuáles son sus limitaciones.

---

### Fase 5: Reporte Final (Obsidian Markdown $\rightarrow$ LaTeX/PDF) y Exposición — `[Richie y Mariana]`
1. **Redacción del reporte en Obsidian Markdown (división 50/50):**
   * **`[Mariana]`** Introducción y planteamiento del problema (justificación de regresión múltiple vs. series de tiempo), descripción clínica de `ASRS` y variables, análisis gráfico/correlaciones ($r$) e interpretación práctica.
   * **`[Richie]`** Descripción técnica de limpieza/integración ($n$ final), desarrollo matemático del modelo MCO (ecuación matricial/escalar, estimadores, $R^2$, pruebas $t$ y $F$), tabla VIF, tabla de coeficientes y diagnóstico de residuales/transformaciones.
   * **`[Mariana y Richie]`** Sección de estimaciones puntuales (mínimo 2 perfiles) y conclusiones generales.
2. **`[Mariana]` Ensamblaje editorial:** Exportar de Obsidian Markdown $\rightarrow$ LaTeX/PDF, verificar formato de ecuaciones, figuras y tablas, y hacer revisión conjunta antes del **miércoles 25 de noviembre (11:59 p.m.)**.
3. **`[Richie y Mariana]` Exposición oral (12–15 min, jueves 26 de noviembre):**
   * **`[Mariana]`** Minutos 1–7: Problema clínico, justificación del modelo, descripción del dataset, EDA, correlaciones e interpretación de variables.
   * **`[Richie]`** Minutos 7–14: Selección por VIF, ecuación MCO, pruebas estadísticas ($R^2, F, t$), diagnóstico/transformaciones, pronósticos puntuales y cierre conjunto.

---

## Flujo de Trabajo en GitHub (2 Personas)

1. Crear o actualizar su rama antes de trabajar:
   ```bash
   git checkout main && git pull
   git checkout -b feature/nombre-tarea
   ```
2. Si agregan una librería nueva, usar siempre `uv add <paquete>` y subir `pyproject.toml` y `uv.lock`.
3. Guardar figuras exportadas en `reports/figures/` y tablas en `reports/tables/` para insertarlas directamente en el reporte.
4. Abrir un Pull Request hacia `main` antes de fusionar.
