# Guion y Estructura de Exposición Oral (12–15 minutos)

**Fecha:** Jueves 26 de noviembre de 2026  
**Equipo:** Mariana (Minutos 1–7) y Richie (Minutos 7–14)  
**Cierre conjunto:** Minuto 14–15  

---

## Parte 1 — Mariana (Minutos 1–7): Contexto clínico, datos, EDA e interpretación práctica

### Diapositiva 1: Portada y Problema Clínico (~1 min)
- **Idea clave:** Evaluar TDAH en adultos es complejo porque depende mucho del autorreporte. Usamos el dataset clínico **HYPERAKTIV** (Hicks et al., 2021) para responder en qué medida la severidad actual (`ASRS`, 0–72) se explica por síntomas infantiles (`WURS`), impulsividad objetiva (`CPT-II Commissions`) y ansiedad (`HADS_A`).

### Diapositiva 2: Por qué Regresión Lineal Múltiple y Metodología CRISP-ML(Q) (~1 min)
- **Por qué MCO y no series de tiempo:** datos de **corte transversal** (cada fila es un paciente único, sin orden temporal), múltiples predictores lineales y $n = 69 \ge 30$ (verificado con $\text{DW} = 2.174$).
- **Flujo reproducible:** 4 notebooks por etapa siguiendo CRISP-ML(Q).

### Diapositiva 3: Descripción Clínica de Variables (~1.5 min)
- `ASRS` ($Y$, 0–72): cribado OMS de severidad actual de TDAH.
- Tres dimensiones complementarias:
  1. `WURS` ($X_1$, 0–100): historia de síntomas en la infancia (corte $\ge 46$).
  2. `General TScore Commissions` ($X_2$, puntaje $T$): impulsividad objetiva en prueba computarizada CPT-II ($T > 60$ elevado).
  3. `HADS_A` ($X_3$, 0–21): ansiedad comórbida ($\ge 11$ clínica).
- **Control de fuga de datos:** excluimos `ID`, `ADHD` y `ADD`.

### Diapositiva 4: EDA — Distribución de `ASRS` y Correlaciones ($r$) (~1.5 min)
- **Figura:** `reports/figures/asrs_distribucion.png` ($n = 75$, media $41.4$, mediana $42$, ligera cola izquierda de 3 pacientes, sin outliers).
- **Correlaciones (Rúbrica 1b):** `WURS` ($r = 0.685$), `Commissions` ($r = 0.526$), `DPrime` ($r = 0.398$), `HADS_A` ($r = 0.304$); `MADRS`, `HADS_D` y `AGE` no significativas.

### Diapositiva 5: Gráficas de Dispersión y Descarte de Candidatas (~1 min)
- **Figura:** `reports/figures/dispersion_candidatas.png` (Rúbrica 1a).
- **Dos hallazgos clave:**
  - `Omissions` ($r = 0.287$) se descartó porque **un solo punto influyente ($\approx 330$)** jalaba la recta.
  - `DPrime` se descartó por alta colinealidad con `Commissions` ($r = 0.88$).

### Diapositiva 6: Interpretación Clínica de Parámetros y Peso por +1 DE (~1 min)
- Transición a Richie: mencionar la interpretación *ceteris paribus* y el impacto de **+1 desviación estándar muestral**:
  - `WURS`: **+7.7 puntos** de `ASRS` (pesa el doble que `Commissions`).
  - `Commissions`: **+3.8 puntos** de `ASRS` (la prueba objetiva aporta valor independiente).
  - `HADS_A`: **+0.6 puntos** (no significativa al controlar por `WURS`).

---

## Parte 2 — Richie (Minutos 7–14): Ingeniería de datos, VIF, MCO, Diagnóstico, Transformaciones y Pronósticos

### Diapositiva 7: Ingeniería de Datos y Validación por VIF (~1.5 min)
- Integración de 3 CSVs (`sep=";"`, `utf-8-sig`), regla de calidad CPT-II (`Raw Score Omissions < 300`), limpieza de 885 columnas $\rightarrow$ $n = 75$ integrados y **$n = 69$ casos completos** (1 nulo en `WURS`, 6 en `HADS_A`).
- **Tabla VIF:** `WURS = 1.623`, `Commissions = 1.390`, `HADS_A = 1.205` — todos $< 2$ (umbral $< 5$), cero multicolinealidad.

### Diapositiva 8: Modelo MCO, Bondad de Ajuste y Pruebas $F$ y $t$ (~1.5 min)
- **Ecuación estimada (Rúbrica 2a):**
  $$\widehat{\text{ASRS}}_i = 7.6350 + 0.3678\,\text{WURS}_i + 0.3079\,\text{Commissions}_i + 0.1273\,\text{HADS\_A}_i$$
- **Evaluación global (Rúbrica 4a y 4b):** $R^2 = 0.5341$, $R^2_{\text{adj}} = 0.5126$, $\text{RMSE} = 9.90$, $F(3, 65) = 24.84$ ($p < 0.001$).
- **Pruebas $t$:** `WURS` ($t = 5.00, p < 0.001$) y `Commissions` ($t = 2.65, p = 0.010$) significativos; `HADS_A` ($p = 0.655$) y `const` ($p = 0.216$) no significativos.

### Diapositiva 9: Real vs. Predicho y Diagnóstico de Residuales (~1.5 min)
- **Figuras:** `ols_real_vs_predicho.png` (Rúbrica 4c) y `ols_residual_diagnostics.png`.
- **Supuestos cumplidos al $\alpha = 0.05$:**
  - Normalidad: Shapiro-Wilk $W = 0.978, p = 0.2634$ (✓).
  - Homocedasticidad: Breusch-Pagan $\text{LM} = 6.77, p = 0.0796$ (✓, aunque cerca del 5 %).
  - Independencia: Durbin-Watson $= 2.174$ (✓).
  - Distancia de Cook: 0 casos $> 1.0$ (✓).

### Diapositiva 10: Transformaciones y Reversión a Escala Original (~1.5 min)
- **Por qué probamos transformaciones (Rúbrica 3a):** por el $p = 0.0796$ de Breusch-Pagan y la no significancia de `HADS_A`.
- **Resultados tras revertir a escala `ASRS` ($\exp(\hat{z}+\hat{\sigma}^2/2)$ y $\hat{z}^2+\hat{\sigma}^2$):**
  - $\ln(\text{ASRS})$ y $\sqrt{\text{ASRS}}$ **estiran la cola izquierda**, rompen normalidad ($p < 0.001$ y $0.013$), empeoran homocedasticidad ($p < 0.03$) y suben el RMSE (`10.51` y `9.73` vs. `9.61`).
  - Quitar `HADS_A` sube $R^2_{\text{adj}}$ a `0.5185`, pero **rompe homocedasticidad** ($p = 0.041 < 0.05$).
- **Decisión:** el **modelo lineal base** es el único que cumple todos los supuestos y minimiza el error.

### Diapositiva 11: Pronósticos en 3 Perfiles Clínicos y Utilidad (~1.5 min)
- **Figura:** `ols_forecasts_profiles.png` (Rúbrica 5a, percentiles P10, P50, P90 sin extrapolación):
  - **Carga baja (P10):** `27.14` (IC media `[22.48, 31.81]`, IP indiv. `[6.82, 47.46]`).
  - **Carga moderada (P50):** `40.31` (IC media `[37.90, 42.72]`, IP indiv. `[20.39, 60.23]`).
  - **Carga alta (P90):** `56.06` (IC media `[51.11, 61.00]`, IP indiv. `[35.67, 72.00]` acotado).
- **Conclusión de cierre (conjunto):** brecha clara de **28.9 puntos** útil para **cribado y estratificación**, pero con IP individual de $\pm 20$ puntos ($\text{RMSE} = 9.9$, 47 % varianza no explicada), por lo que complementa y no sustituye la entrevista clínica.

---

## Banco de Preguntas Posibles del Profesor (Q&A)

1. **¿Por qué dejaron `HADS_A` en el modelo final si su $p$-valor fue $0.6547$?**
   - Porque al eliminarla (modelo parsimonioso) se rechaza la homocedasticidad en Breusch-Pagan ($p = 0.0411 < 0.05$), mientras que mantenerla preserva todos los supuestos clásicos al 5 %, reduce ligeramente el RMSE (`9.6102` vs. `9.6251`) y controla clínicamente por la comorbilidad ansiosa.
2. **¿Por qué empeoró el modelo al aplicar $\ln(\text{ASRS})$?**
   - Porque el logaritmo corrige asimetría positiva (cola derecha), pero `ASRS` tenía una ligera cola izquierda (3 pacientes con puntajes 6–10). El logaritmo separó aún más esos valores bajos del resto, destruyendo la normalidad de residuales (Shapiro-Wilk $p < 0.0001$).
3. **¿Cómo evitaron extrapolación en los pronósticos?**
   - Construyendo los tres perfiles con los percentiles P10, P50 y P90 de la muestra efectiva ($n = 69$), garantizando que todos los valores estén estrictamente dentro del rango observado de cada predictor.
4. **¿Por qué el límite superior del IP 95 % en Carga Alta dio 76.44 si `ASRS` llega a 72?**
   - Porque MCO asume una respuesta continua no acotada en $(-\infty, +\infty)$. En la interpretación clínica se reporta tanto el valor estadístico (`76.44`) como el intervalo acotado al dominio real de la escala (`72.00`).

