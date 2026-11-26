# Notas para el Presentador — Exposición ARC

**Presentación:** `presentacion_arc_marp` (12 diapositivas · 12–15 minutos)  
**Expositores:** Mariana Salazar (Diapositivas 1–6) · Luis Alejandro Luna Martínez / Richie (Diapositivas 7–12)  
**Materia:** Análisis de Regresión y Correlación (ARC) — UABC

---

## Parte 1 — Mariana (Diapositivas 1 a 6 · ~7 min)

### Diapositiva 1: Portada — Severidad de Síntomas de TDAH en Adultos (`ASRS`) (~1 min)
- El TDAH inicia en la infancia y suele persistir en la adultez.
- Evaluarlo en adultos es complejo porque depende mucho del **autorreporte**.
- Dataset clínico **HYPERAKTIV** (Hicks et al., 2021).
- **Pregunta:** ¿Cuánto de la severidad actual (`ASRS`) se explica por síntomas infantiles (`WURS`), impulsividad objetiva (`CPT-II`) y ansiedad (`HADS_A`)?

### Diapositiva 2: ¿Por qué Regresión Lineal Múltiple y CRISP-ML(Q)? (~1 min)
- **Corte transversal (no series de tiempo):** cada fila es un paciente único evaluado una sola vez, sin orden temporal.
- **Requisitos cumplidos:** más de 2 predictores, **`n = 69 ≥ 30`** y **`Durbin-Watson = 2.174`** (sin autocorrelación).
- **Metodología CRISP-ML(Q):** flujo reproducible en **4 notebooks** (`01` a `04`).

### Diapositiva 3: Variables Clínicas y Control de Fuga de Datos (~1.5 min)
- **$Y$ (`ASRS`):** escala OMS de severidad actual (`0–72`, 18 ítems DSM). Mayor puntaje = mayor severidad.
- **3 dimensiones complementarias:**
  - $X_1$ **`WURS`** (`0–100`): síntomas retrospectivos en infancia (corte orientativo `≥ 46`).
  - $X_2$ **`Commissions`** (puntaje $T$): impulsividad objetiva en prueba computarizada CPT-II (`T > 60` elevado).
  - $X_3$ **`HADS_A`** (`0–21`): ansiedad comórbida (`≥ 11` clínica).
- **Control de fuga de datos:** excluimos `ID`, `ADHD` y `ADD` porque equivalen al diagnóstico mismo.

### Diapositiva 4: EDA — Distribución de `ASRS` y Correlaciones ($r$) (~1.5 min)
- **Señalar gráfica (izq.):** `n = 75`, media **`41.4`**, mediana **`42.0`**, distribución simétrica y **sin atípicos** (ligera cola izquierda de 3 pacientes).
- **Señalar tabla (der.):**
  - **`WURS` (`r = 0.685`, `p < 0.001`):** correlación fuerte.
  - **`Commissions` (`r = 0.526`, `p < 0.001`):** prueba objetiva conectada con autorreporte.
  - **`HADS_A` (`r = 0.304`, `p = 0.011`):** significativa débil-moderada.
  - **`MADRS`, `HADS_D` y `AGE`:** no significativas (`p > 0.15`).

### Diapositiva 5: Gráficas de Dispersión y Descarte de Candidatas (~1 min)
- **Regla clave:** siempre graficar, no confiar solo en $r$.
- **`Omissions` (`r = 0.287`) descartada:** un solo paciente extremo (`≈ 330`) jalaba la recta; sin él, la relación desaparece.
- **`DPrime` (`r = 0.398`) descartada:** alta colinealidad con `Commissions` (**`r = 0.88`**) dentro del mismo test CPT-II.

### Diapositiva 6: Impacto Clínico — Peso por +1 Desviación Estándar (~1 min)
- Como las escalas son distintas, comparamos el efecto de **+1 DE muestral** (*ceteris paribus*):
  - **`WURS`:** **`+7.7 pts`** de `ASRS` (pesa el doble que `Commissions`).
  - **`Commissions`:** **`+3.8 pts`** (aporta señal objetiva independiente).
  - **`HADS_A`:** **`+0.6 pts`** (efecto marginal al controlar por las otras dos).
- *Transición:* ceder la palabra a Richie.

---

## Parte 2 — Richie (Diapositivas 7 a 12 · ~7–8 min)

### Diapositiva 7: Ingeniería de Datos y Validación por `VIF` (~1.5 min)
- **Integración:** *inner join* de 3 CSVs por `ID` (`sep=";"`, `utf-8-sig`).
- **Filtro de calidad CPT-II:** `Raw Score Omissions < 300` para descartar sesiones inválidas.
- **Depuración:** `885` columnas → `n = 75` integrados → **`n = 69` casos completos** (1 nulo en `WURS`, 6 en `HADS_A`).
- **Multicolinealidad (`VIF`):** `WURS = 1.623`, `Commissions = 1.390`, `HADS_A = 1.205` — todos **`< 2`** (umbral `< 5`).

### Diapositiva 8: Modelo MCO Estimado, Bondad de Ajuste y Pruebas $F$ / $t$ (~1.5 min)
- **Ecuación:** $\widehat{\text{ASRS}} = 7.6350 + 0.3678\,\text{WURS} + 0.3079\,\text{Commissions} + 0.1273\,\text{HADS\_A}$.
- **Ajuste global:** **`R² = 53.41 %`** (`R²_adj = 0.5126`), **`RMSE = 9.90`**.
- **Prueba $F(3, 65)$:** **`24.84`** (`p = 8.00e-11`, altamente significativo).
- **Pruebas $t$:** `WURS` (`p < 0.001`) y `Commissions` (`p = 0.010`) significativos; `HADS_A` (`p = 0.655`) y `const` (`p = 0.216`) no significativos.

### Diapositiva 9: Ajuste Real vs. Predicho y Diagnóstico de Residuales (~1.5 min)
- **Real vs. predicho (izq.):** puntos alineados a la diagonal identidad sin curvaturas.
- **Supuestos cumplidos (`α = 0.05`):**
  - **Normalidad:** Shapiro-Wilk **`p = 0.2634`** (✓).
  - **Homocedasticidad:** Breusch-Pagan **`p = 0.0796`** (✓, cerca del 5 %).
  - **Independencia:** **`DW = 2.174`** (✓).
  - **Influyentes:** Cook **`0 casos > 1`** (✓).
- Ese `p = 0.0796` y el $p$ de `HADS_A` motivaron probar transformaciones.

### Diapositiva 10: Transformaciones y Reversión a Escala Original (~1.5 min)
- **Comparación justa:** se revirtieron $\ln(\text{ASRS})$ y $\sqrt{\text{ASRS}}$ a escala original (`e^(z + σ²/2)` y `z² + σ²`).
- **$\ln(\text{ASRS})$ y $\sqrt{\text{ASRS}}$:** estiran la cola izquierda, **rompen normalidad** (`p < 0.001` y `0.013`), empeoran homocedasticidad y suben el `RMSE`.
- **Sin `HADS_A`:** sube ligeramente $R^2_{\text{adj}}$, pero **rompe homocedasticidad** (`p = 0.041 < 0.05`).
- **Decisión:** el **modelo lineal base** es el único que cumple todos los supuestos y minimiza el error (**`RMSE = 9.61`**).

### Diapositiva 11: Pronósticos en 3 Perfiles Clínicos y Conclusión (~1.5 min)
- **Sin extrapolación:** perfiles basados en percentiles **P10, P50 y P90** de la muestra (`n = 69`):
  - **Carga baja (P10):** **`27.14`** (IC `[22.48, 31.81]`, IP `[6.82, 47.46]`).
  - **Carga moderada (P50):** **`40.31`** (IC `[37.90, 42.72]`, IP `[20.39, 60.23]`).
  - **Carga alta (P90):** **`56.06`** (IC `[51.11, 61.00]`, IP `[35.67, 72.00]` acotado al máximo clínico `72`).
- **Cierre conjunto:**
  - Brecha de **`28.9` puntos** útil para **cribado y estratificación**.
  - IP individual de **`±20` puntos** (~47 % varianza no explicada) → **complementa, no sustituye** la entrevista clínica.

### Diapositiva 12: Cierre — ¡Muchas Gracias por su Atención!
- Agradecer y abrir ronda de preguntas.

---

## Banco Rápido de Preguntas (Q&A)

- **¿Por qué dejaron `HADS_A` si su $p$-valor fue `0.655`?**
  - Al quitarla se rechaza homocedasticidad en Breusch-Pagan (`p = 0.041 < 0.05`).
  - Mantenerla preserva todos los supuestos al 5 %, reduce el `RMSE` (`9.61` vs. `9.63`) y controla clínicamente por ansiedad.
- **¿Por qué empeoró $\ln(\text{ASRS})$?**
  - El logaritmo corrige colas derechas, pero `ASRS` tenía una ligera cola izquierda (3 pacientes con `6–10`).
  - Separó esos puntajes bajos y destruyó la normalidad de residuales (`p < 0.001`).
- **¿Cómo evitaron extrapolación en los pronósticos?**
  - Usando únicamente percentiles observados (**P10, P50, P90**) de la muestra efectiva (`n = 69`).
- **¿Por qué el IP 95 % en Carga Alta llega a `76.44` si `ASRS` llega a `72`?**
  - MCO asume respuesta continua no acotada en $(-\infty, +\infty)$; reportamos el valor estadístico (`76.44`) y el acotado al dominio real (`72.00`).
