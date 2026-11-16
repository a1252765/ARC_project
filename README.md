# Proyecto Final — Análisis de Regresión y Correlación (ARC)

Modelado de la severidad de síntomas de TDAH en adultos (`ASRS`) en el dataset clínico **HYPERAKTIV** (Hicks et al., 2021) mediante **Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO)**.

## Equipo y Roles

* **Richie:** Ingeniería de datos, notebooks de análisis, modelado MCO (`statsmodels`), diagnóstico de supuestos y pronósticos.
* **Mariana:** Análisis exploratorio (EDA), interpretación clínica/estadística, redacción del reporte (Obsidian Markdown + LaTeX $\rightarrow$ PDF) y coordinación de entregables.

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

### Fase 0: Rama Limpia, Datos y Estructura
1. **Crear una rama nueva desde `main`** para construir el análisis desde cero:
   ```bash
   git checkout main && git pull
   git checkout -b feature/analisis-desde-cero
   ```
2. **Verificar que los 3 CSV existen en `data/raw/`** (separador `;` y codificación `utf-8-sig` en el archivo de CPT-II).
3. **Crear la carpeta `notebooks/`** con tres notebooks secuenciales:
   * `notebooks/01_eda_y_seleccion.ipynb`
   * `notebooks/02_modelo_mco_y_evaluacion.ipynb`
   * `notebooks/03_transformaciones_y_pronosticos.ipynb`

---

### Fase 1: Integración de Datos, EDA y Selección de Predictores (Rúbrica 1)
**Objetivo:** Justificar el enfoque de regresión lineal múltiple ($n \ge 30$, al menos 2 variables independientes), limpiar los datos, analizar gráficas de dispersión y seleccionar 3–4 predictores con sentido clínico y sin multicolinealidad.

1. **Carga e integración por `ID`:**
   * Cargar `patient_info.csv`, `features.csv` y `CPT_II_ConnersContinuousPerformanceTest.csv` (`sep=";"`).
   * Revisar duplicados por `ID`, valores faltantes y tipos de datos.
   * Aplicar regla de calidad en CPT-II: filtrar sesiones inválidas (por ejemplo, `Raw Score Omissions >= 300`, donde el paciente no respondió o se desconectó el teclado).
   * Unir las tablas por `ID` (inner join) y descartar filas sin `ASRS` (variable respuesta $Y$). Verificar que $n \ge 30$.
2. **Análisis gráfico (Rúbrica 1a):**
   * Graficar la distribución de `ASRS` (histograma + boxplot).
   * Generar **gráficas de dispersión** ($X_i$ vs `ASRS`) con línea de tendencia para las variables candidatas, observando si la relación parece lineal o curva y si hay varianza creciente (heterocedasticidad) o valores atípicos.
3. **Cálculo e interpretación de correlación $r$ (Rúbrica 1b):**
   * Calcular la matriz de correlación de Pearson ($r$) y los $p$-valores respecto a `ASRS`.
   * Excluir variables que sean identificadores (`ID`) o diagnósticos directos redundantes si generan fuga de información (`ADHD`, `ADD`).
   * Interpretar dirección, magnitud y significancia estadística de cada $r$.
4. **Selección híbrida de 3–4 predictores y control de multicolinealidad (VIF):**
   * Elegir **3 a 4 variables independientes** ($X_1, X_2, X_3, \dots$) combinando:
     * Relevancia clínica/teórica respecto a síntomas de TDAH (`ASRS`).
     * Correlación clara con `ASRS`.
     * Baja colinealidad entre predictores: calcular el **Factor de Inflación de Varianza (VIF)** con `statsmodels.stats.outliers_influence.variance_inflation_factor` y verificar que **$\text{VIF} < 5$** para todos los predictores elegidos.
   * Guardar el dataset limpio e integrado en `data/processed/` para usarlo en los siguientes notebooks.

---

### Fase 2: Construcción del Modelo MCO e Interpretación (Rúbrica 2 y 4a–4b)
**Objetivo:** Plantear formalmente el modelo, estimarlo por MCO en `statsmodels`, interpretar cada parámetro y evaluarlo estadísticamente.

1. **Planteamiento formal de la ecuación (Rúbrica 2a):**
   $$\widehat{\text{ASRS}}_i = \hat{\beta}_0 + \hat{\beta}_1 X_{1i} + \hat{\beta}_2 X_{2i} + \dots + \hat{\beta}_k X_{ki}$$
   Documentar el significado y unidades de $Y$ y de cada $X_j$.
2. **Ajuste MCO en `statsmodels`:**
   * Añadir constante (`sm.add_constant`) y ajustar `sm.OLS(y, X).fit()`.
   * Extraer la tabla resumen (`.summary()`).
3. **Interpretación teórica y práctica de parámetros (Rúbrica 2b):**
   * **Intercepto ($\hat{\beta}_0$):** valor esperado de `ASRS` cuando todos los predictores son 0 (indicar si tiene sentido clínico o solo matemático).
   * **Pendientes ($\hat{\beta}_j$):** cambio esperado en `ASRS` por cada incremento de 1 unidad en $X_j$, manteniendo constantes las demás variables (*ceteris paribus*).
4. **Evaluación global e individual (Rúbrica 4a y 4b):**
   * **$R^2$ y $R^2_{\text{ajustado}}$:** porcentaje de la variabilidad de `ASRS` explicado por el modelo (y por qué el ajustado penaliza predictores innecesarios).
   * **Prueba global $F$:** $H_0: \beta_1 = \beta_2 = \dots = \beta_k = 0$. Verificar $p < 0.05$.
   * **Pruebas individuales $t$:** $H_0: \beta_j = 0$ para cada coeficiente, sus $p$-valores e intervalos de confianza al 95%.

---

### Fase 3: Diagnóstico Gráfico, Transformaciones y Comparación (Rúbrica 3a y 4c)
**Objetivo:** Verificar si se cumplen los supuestos del modelo lineal, aplicar transformaciones solo si es necesario y graficar valores reales vs. ajustados.

1. **Diagnóstico de residuales:**
   * Graficar residuales vs. valores ajustados (detectar no linealidad o forma de embudo/varianza creciente).
   * Graficar Q-Q plot / histograma de residuales (normalidad) y revisar puntos influyentes (distancia de Cook).
2. **Transformaciones (Rúbrica 3a — si aplica):**
   * Si en las gráficas se observa relación no lineal o varianza creciente, probar transformaciones (por ejemplo, $\ln(Y)$, $\sqrt{Y}$, o $\ln(X_j)$ / términos cuadráticos) y comparar el $R^2_{\text{ajustado}}$ y los residuales frente al modelo base.
   * **Importante:** Si se transforma $Y$, documentar cómo se **revierte la transformación** para obtener los pronósticos en la escala original de `ASRS` (por ejemplo, $\hat{Y} = \exp(\widehat{\ln Y})$ o ajuste por $\exp(\hat{\sigma}^2 / 2)$).
3. **Gráfica del modelo de regresión vs. datos reales (Rúbrica 4c):**
   * Graficar `ASRS` real vs. $\widehat{\text{ASRS}}$ predicho con la línea identidad ($y = x$) para mostrar visualmente el ajuste del modelo.

---

### Fase 4: Estimaciones Puntuales y Pronósticos (Rúbrica 5a)
**Objetivo:** Realizar al menos dos estimaciones puntuales con el modelo final y evaluar su utilidad práctica.

1. **Definir al menos 2 perfiles de pacientes** (dentro del rango observado de los datos para evitar extrapolación inválida): por ejemplo, un perfil con carga sintomática/conductual baja y otro con carga alta.
2. **Calcular las estimaciones puntuales** (y opcionalmente sus intervalos de confianza y predicción al 95% con `.get_prediction()`).
3. **Si hubo transformación en $Y$**, mostrar explícitamente el cálculo de reversión a la escala original de `ASRS`.
4. **Redactar conclusión de utilidad:** qué tan precisas son las estimaciones, qué aporta el modelo en contexto clínico y cuáles son sus limitaciones.

---

### Fase 5: Reporte Final (Obsidian Markdown $\rightarrow$ LaTeX/PDF) y Exposición
1. **Estructura del reporte en Obsidian Markdown:**
   * Introducción y planteamiento del problema (justificación de regresión múltiple vs. series de tiempo).
   * Descripción de la base de datos HYPERAKTIV, limpieza y tamaño de muestra final ($n$).
   * Desarrollo matemático del modelo MCO (ecuación matricial/escalar, estimadores, $R^2$, pruebas $t$ y $F$).
   * Análisis gráfico y tabla de correlaciones ($r$, $p$-valores) + tabla de VIF.
   * Resultados del modelo MCO, tabla de coeficientes e interpretación teórica/práctica.
   * Diagnóstico de supuestos, transformaciones (si aplica) y gráfica de valores reales vs. predichos.
   * Estimaciones puntuales (mínimo 2) y conclusiones.
2. **Exportación a LaTeX / PDF** y revisión conjunta antes del **miércoles 25 de noviembre (11:59 p.m.)**.
3. **Preparar presentación de 12–15 min** (problema, justificación, gráficas clave, pronósticos y conclusiones) para el **jueves 26 de noviembre**.

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
