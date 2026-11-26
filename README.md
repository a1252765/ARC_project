# Modelado de la Severidad de Síntomas de TDAH en Adultos (`ASRS`) mediante Regresión Lineal Múltiple (MCO)

**Universidad Autónoma de Baja California (UABC)** — Licenciatura en Ciencia de Datos  
**Materia:** Análisis de Regresión y Correlación (ARC)  
**Profesora:** Cynthia Calderón García  
**Equipo:** Luis Alejandro Luna Martínez & Mariana Salazar  

> La guía paso a paso original de planeación, distribución de roles y bitácora operativa de desarrollo se conservó en [docs/BITACORA_GUIA_DESARROLLO.md](docs/BITACORA_GUIA_DESARROLLO.md).

---

## 1. Descripción del Proyecto

Este repositorio implementa un flujo reproducible de ciencia de datos para modelar la severidad autorreportada de síntomas de Trastorno por Déficit de Atención e Hiperactividad (TDAH) en adultos —medida mediante la escala **`ASRS`** (0–72 puntos)— utilizando el conjunto de datos clínico **HYPERAKTIV** (Hicks et al., 2021).

**Pregunta de investigación:**  
*¿En qué medida la severidad actual de síntomas de TDAH en adultos (`ASRS`) puede explicarse a partir de los síntomas retrospectivos en la infancia (`WURS`), el desempeño objetivo en una prueba computarizada de impulsividad (`General TScore Commissions` del CPT-II) y la sintomatología de ansiedad comórbida (`HADS_A`)?*

---

## 2. Justificaciones Teóricas y Metodológicas

### 2.1 ¿Por qué Regresión Lineal Múltiple (MCO) y no Series de Tiempo?
- **Naturaleza de los datos (corte transversal):** cada observación en HYPERAKTIV corresponde a un paciente distinto evaluado en una única sesión clínica; no existe orden cronológico ni mediciones repetidas longitudinales de un mismo sujeto.
- **Objetivo inferencial:** se busca cuantificar la relación marginal (*ceteris paribus*) entre múltiples predictores continuos y una variable respuesta continua (`ASRS`), cumpliendo con $n = 69 \ge 30$ casos completos.
- **Verificación empírica de independencia:** el estadístico de Durbin-Watson sobre los residuales ($\text{DW} = 2.174$) confirma la ausencia de autocorrelación.

### 2.2 Marco Metodológico CRISP-ML(Q) y Prevención de Fuga de Datos
El análisis se organizó en **4 cuadernos secuenciales** bajo el estándar **CRISP-DM / CRISP-ML(Q)** (*Cross-Industry Standard Process for Machine Learning with Quality Assurance*):
- **Calidad de datos:** integración relacional por `ID` de las tres tablas crudas (`patient_info`, `features`, `CPT_II`), aplicando el filtro clínico `Raw Score Omissions < 300` para descartar pruebas CPT-II inválidas ($n = 75$ integrados; $n = 69$ casos completos).
- **Prevención de fuga de información (*data leakage*):** se excluyeron explícitamente el identificador `ID` y las etiquetas diagnósticas directas (`ADHD`, `ADD`), ya que equivalen al diagnóstico objetivo mismo.

### 2.3 Fundamento Clínico y Psicométrico de las Variables
Los tres predictores seleccionados cubren dimensiones complementarias del cuadro clínico del TDAH adulto:
1. **`WURS`** (*Wender Utah Rating Scale*, 0–100): evalúa síntomas retrospectivos en la infancia (corte orientativo $\ge 46$), capturando la continuidad neuroevolutiva del trastorno.
2. **`General TScore Commissions`** (*Conners' CPT-II*, puntaje $T$ con $\mu = 50, \sigma = 10$): mide errores de comisión (responder ante estímulos no-objetivo), aportando un indicador conductual objetivo de impulsividad/desinhibición ($T > 60$ elevado).
3. **`HADS_A`** (*Hospital Anxiety and Depression Scale*, 0–21): mide ansiedad comórbida (0–7 normal, 8–10 limítrofe, $\ge 11$ clínica), frecuente en adultos evaluados por TDAH.

### 2.4 Criterios Estadísticos de Selección de Variables y Control de Colinealidad
- **Complementariedad entre correlación de Pearson ($r$) y análisis gráfico:** se descartó `General TScore Omissions` ($r = 0.287$) porque la gráfica de dispersión reveló que su correlación estaba inflada por un único paciente extremo ($\approx 330$).
- **Eliminación de redundancia:** se detectó colinealidad severa entre `Commissions` y `DPrime` ($r = 0.88$), conservando `Commissions` por su mayor asociación con `ASRS` ($r = 0.526$ vs. $0.398$) e interpretación directa.
- **Factor de Inflación de Varianza (VIF):** se verificó $\text{VIF}_j = \frac{1}{1 - R_j^2} < 5$ para todos los predictores (`WURS = 1.623`, `General TScore Commissions = 1.390`, `HADS_A = 1.205`), descartando multicolinealidad.

### 2.5 Formulación Matemática MCO y Supuestos de Gauss-Markov
El modelo lineal poblacional en forma escalar y matricial es:

$$\text{ASRS}_i = \beta_0 + \beta_1\,\text{WURS}_i + \beta_2\,\text{Commissions}_i + \beta_3\,\text{HADS\_A}_i + \varepsilon_i, \qquad \mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$$

bajo $\mathbb{E}[\varepsilon_i \mid \mathbf{X}] = 0$, $\text{Var}(\varepsilon_i \mid \mathbf{X}) = \sigma^2$, $\text{Cov}(\varepsilon_i, \varepsilon_j \mid \mathbf{X}) = 0$ ($i \neq j$) y $\varepsilon_i \sim \mathcal{N}(0, \sigma^2)$. El estimador de Mínimos Cuadrados Ordinarios minimiza la suma de cuadrados residual y tiene solución cerrada:

$$\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}$$

### 2.6 Justificación Teórica de Transformaciones y Selección del Modelo Final
Para contrastar si una transformación estabilizaba la varianza (dado Breusch-Pagan $p = 0.0796$), se evaluaron $\ln(\text{ASRS})$ y $\sqrt{\text{ASRS}}$ revirtiendo sus predicciones a la escala original de `ASRS` ($\widehat{Y} = \exp(\widehat{\ln Y} + \hat{\sigma}^2/2)$ y $\widehat{Y} = (\widehat{\sqrt{Y}})^2 + \hat{\sigma}^2$), así como un modelo parsimonioso sin `HADS_A`:
- Las transformaciones cóncavas ($\ln$ y $\sqrt{\cdot}$) corrigen sesgos positivos (cola derecha), pero `ASRS` presenta una ligera **cola izquierda** (3 puntajes entre 6 y 10); aplicarlas violó la normalidad (Shapiro-Wilk $p < 0.0001$ y $p = 0.0127$), empeoró la homocedasticidad ($p < 0.03$) y aumentó el RMSE en escala original.
- Eliminar `HADS_A` incumplió homocedasticidad al 5 % (Breusch-Pagan $p = 0.0411$).
- **Decisión:** se conservó el **modelo lineal base en escala original (3 predictores)** por ser la única especificación que cumple simultáneamente todos los supuestos clásicos y minimiza el error en puntos `ASRS`.

---

## 3. Resultados Principales

**Ecuación estimada ($n = 69$):**

$$\widehat{\text{ASRS}}_i = 7.6350 + 0.3678\,\text{WURS}_i + 0.3079\,\text{Commissions}_i + 0.1273\,\text{HADS\_A}_i$$

| Métrica / Prueba | Resultado | Conclusión |
|---|---|---|
| $R^2$ / $R^2_{\text{ajustado}}$ | `0.5341` / `0.5126` | Explica el 53.41 % de la variabilidad de `ASRS` ($\text{RMSE} = 9.90$) |
| Prueba $F(3, 65)$ | `24.8355` ($p = 8.00 \times 10^{-11}$) | Modelo globalmente significativo |
| Significancia individual ($t$) | `WURS` ($p < 0.0001$), `Commissions` ($p = 0.0101$), `HADS_A` ($p = 0.6547$) | `WURS` pesa $\approx 2\times$ más que `Commissions` por +1 DE (+7.7 vs. +3.8 pts) |
| Normalidad (Shapiro-Wilk) | $W = 0.9780$ ($p = 0.2634$) | Cumple normalidad ($\alpha = 0.05$) |
| Homocedasticidad (Breusch-Pagan) | $\text{LM} = 6.7705$ ($p = 0.0796$) | Cumple homocedasticidad ($\alpha = 0.05$) |
| Independencia (Durbin-Watson) | $\text{DW} = 2.174$ | Sin autocorrelación |
| Distancia de Cook | 0 casos $> 1.0$ (5 casos $> 4/n$) | Ajuste estable sin observaciones patológicas |

**Pronósticos puntuales en 3 perfiles clínicos (percentiles P10, P50 y P90, sin extrapolación):**
- **Carga baja (P10):** $\widehat{\text{ASRS}} = 27.14$ — IC 95 % media `[22.48, 31.81]` | IP 95 % indiv. `[6.82, 47.46]`
- **Carga moderada (P50):** $\widehat{\text{ASRS}} = 40.31$ — IC 95 % media `[37.90, 42.72]` | IP 95 % indiv. `[20.39, 60.23]`
- **Carga alta (P90):** $\widehat{\text{ASRS}} = 56.06$ — IC 95 % media `[51.11, 61.00]` | IP 95 % indiv. `[35.67, 72.00]` *(acotado al techo de la escala)*

---

## 4. Estructura del Repositorio y Reproducibilidad

```text
ARC_project/
├── data/
│   ├── raw/                             # CSVs originales de HYPERAKTIV (ignorados en Git)
│   └── processed/hyperaktiv_arc_clean.csv
├── notebooks/
│   ├── 01_data_ingestion_and_cleaning.ipynb
│   ├── 02_eda_and_feature_selection.ipynb
│   ├── 03_ols_modeling_and_diagnostics.ipynb
│   └── 04_transformations_and_forecasting.ipynb
├── reports/
│   ├── figures/                         # 5 figuras oficiales exportadas
│   ├── tables/                          # Tablas CSV oficiales (correlaciones, VIF, MCO, pronósticos)
│   └── reporte_final/
│       ├── reporte_final_arc.pdf        # Reporte final compilado en LaTeX (13 páginas)
│       ├── reporte_final_arc.tex
│       └── reporte_final_arc.md
└── docs/
    ├── BITACORA_GUIA_DESARROLLO.md      # Bitácora original de planeación y flujo de trabajo
    ├── METODOLOGIA_CRISP_ML.md          # Detalle por fase CRISP-ML(Q)
    └── GUION_EXPOSICION.md              # Guion 50/50 para defensa oral y Q&A
```

**Reproducción del entorno con `uv`:**
```bash
uv sync
uv run jupyter lab
```

---

## 5. Referencias (APA 7.ª edición)

Conners, C. K. (2000). *Conners' Continuous Performance Test II (CPT II) computer program for Windows technical guide and software manual*. Multi-Health Systems.

Hicks, S. A., Stautland, A., Fasmer, O. B., Førland, W., Hammer, H. L., Halvorsen, P., Mjeldheim, K., Oedegaard, K. J., Osnes, B., Syrstad, V. E. G., Riegler, M. A., & Jakobsen, P. (2021). HYPERAKTIV: An activity dataset from adult patients with attention-deficit/hyperactivity disorder (ADHD). En *Proceedings of the 12th ACM Multimedia Systems Conference (MMSys '21)*. Association for Computing Machinery. https://doi.org/10.1145/3458305.3478454

Kessler, R. C., Adler, L., Ames, M., Demler, O., Faraone, S. A., Hiripi, E., Gruber, M. J., Houle, J. J., Merikangas, K. R., Wand, O. M., & Zaslavsky, A. M. (2005). The World Health Organization adult ADHD self-report scale (ASRS): A short screening scale for use in the general population. *Psychological Medicine*, *35*(2), 245–256. https://doi.org/10.1017/S0033291704002892

Ward, M. F., Wender, P. H., & Reimherr, F. W. (1993). The Wender Utah Rating Scale: An aid in the retrospective diagnosis of childhood attention deficit hyperactivity disorder. *The American Journal of Psychiatry*, *150*(6), 885–890. https://doi.org/10.1176/ajp.150.6.885

Zigmond, A. S., & Snaith, R. P. (1983). The Hospital Anxiety and Depression Scale. *Acta Psychiatrica Scandinavica*, *67*(6), 361–370. https://doi.org/10.1111/j.1600-0447.1983.tb09716.x
