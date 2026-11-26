---
marp: true
theme: default
size: 16:9
paginate: true
math: katex
footer: "UABC · Análisis de Regresión y Correlación · Proyecto Final HYPERAKTIV"
---

<style>
:root {
  --navy: #1E3A5F;
  --navy-dark: #0F2540;
  --sky: #E0F2FE;
  --bg: #F8FAFC;
  --card: #FFFFFF;
  --amber: #D97706;
  --amber-soft: #FEF3C7;
  --text: #1E293B;
  --muted: #64748B;
  --border: #E2E8F0;
}

section {
  font-family: 'Inter', 'Noto Sans', 'Ubuntu', 'Liberation Sans', sans-serif;
  background-color: var(--bg);
  color: var(--text);
  padding: 44px 56px;
  font-size: 24px;
  line-height: 1.4;
}

/* Portada y Cierre */
section.lead {
  background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 55%, #DBEAFE 100%);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

section.lead .badge {
  display: inline-block;
  background: #FFFFFF;
  color: var(--navy);
  border: 1px solid #BFDBFE;
  border-radius: 999px;
  padding: 6px 18px;
  font-size: 0.65em;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 18px;
  box-shadow: 0 2px 8px rgba(30, 58, 95, 0.06);
}

section.lead h1 {
  font-family: 'Playfair Display', 'Georgia', 'Liberation Serif', serif;
  color: var(--navy-dark);
  font-size: 2.05em;
  line-height: 1.15;
  margin: 0 0 16px 0;
  font-weight: 700;
}

section.lead .subtitle {
  font-size: 0.92em;
  color: #334155;
  max-width: 900px;
  margin: 0 auto 26px auto;
  line-height: 1.45;
}

section.lead .divider {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, var(--navy), var(--amber));
  border-radius: 2px;
  margin: 0 auto 24px auto;
}

section.lead .meta {
  font-size: 0.72em;
  color: var(--muted);
  line-height: 1.65;
}

section.lead .meta strong {
  color: var(--navy);
}

/* Encabezados de diapositivas */
.speaker-tag {
  display: inline-block;
  font-size: 0.52em;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--amber);
  background: var(--amber-soft);
  padding: 3px 10px;
  border-radius: 6px;
  margin-bottom: 6px;
}

h2 {
  font-family: 'Playfair Display', 'Georgia', 'Liberation Serif', serif;
  color: var(--navy-dark);
  font-size: 1.38em;
  margin: 0 0 18px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border);
  position: relative;
}

h2::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 72px;
  height: 3px;
  background: var(--amber);
  border-radius: 2px;
}

strong {
  color: var(--navy);
}

/* Layouts y Tarjetas */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: center;
}

.grid-2-asym {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 24px;
  align-items: center;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 14px;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 22px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}

.card-accent {
  border-left: 4px solid var(--amber);
}

.card-navy {
  border-left: 4px solid var(--navy);
}

.kpi-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-top: 4px solid var(--navy);
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}

.kpi-card.amber {
  border-top-color: var(--amber);
}

.kpi-card.muted {
  border-top-color: #94A3B8;
  opacity: 0.88;
}

.kpi-val {
  font-size: 2.0em;
  font-weight: 800;
  color: var(--navy-dark);
  line-height: 1.1;
  margin-bottom: 6px;
}

.kpi-card.amber .kpi-val {
  color: var(--amber);
}

.kpi-card.muted .kpi-val {
  color: var(--muted);
}

.kpi-title {
  font-size: 0.78em;
  font-weight: 700;
  color: var(--navy);
}

.kpi-desc {
  font-size: 0.62em;
  color: var(--muted);
  margin-top: 4px;
}

/* Fórmula destacada */
.formula-box {
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-left: 5px solid var(--navy);
  border-radius: 10px;
  padding: 12px 20px;
  text-align: center;
  font-size: 0.92em;
  margin: 10px 0 16px 0;
  box-shadow: 0 2px 10px rgba(30, 58, 95, 0.05);
}

/* Flujo CRISP-ML */
.flow {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  margin: 18px 0 12px 0;
}

.flow-step {
  flex: 1;
  background: #FFFFFF;
  border: 1px solid #CBD5E1;
  border-top: 3px solid var(--navy);
  border-radius: 10px;
  padding: 12px 8px;
  text-align: center;
  font-size: 0.66em;
  font-weight: 700;
  color: var(--navy-dark);
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
}

.flow-arrow {
  color: var(--amber);
  font-weight: 800;
  font-size: 0.9em;
}

/* Tablas */
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.72em;
  background: #FFFFFF;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05);
}

th {
  background-color: var(--navy);
  color: #FFFFFF;
  font-weight: 600;
  text-align: left;
  padding: 9px 12px;
}

td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
}

tr:nth-child(even) td {
  background-color: #F8FAFC;
}

tr.hl td {
  background-color: #EFF6FF;
  font-weight: 700;
  color: var(--navy-dark);
}

tr.muted-row td {
  color: #94A3B8;
}

/* Imágenes */
.fig-wrap {
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px;
  box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
  text-align: center;
}

.fig-wrap img {
  max-width: 100%;
  max-height: 400px;
  display: block;
  margin: 0 auto;
  border-radius: 6px;
}

.note-bar {
  margin-top: 14px;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 8px;
  padding: 9px 14px;
  font-size: 0.70em;
  color: var(--navy-dark);
}

.note-bar.amber {
  background: #FFFBEB;
  border-color: #FDE68A;
  color: #78350F;
}

code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  background: #E2E8F0;
  color: var(--navy-dark);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.88em;
}

footer {
  color: #94A3B8;
  font-size: 0.56em;
}

section::after {
  color: #64748B;
  font-size: 0.62em;
  font-weight: 600;
}

.siglas {
  margin-top: 10px;
  font-size: 0.52em;
  color: #64748B;
  line-height: 1.35;
}
</style>

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge">UABC (Universidad Autónoma de Baja California) · Licenciatura en Ciencia de Datos</div>

# Severidad de Síntomas de TDAH en Adultos (`ASRS`)

<div class="subtitle">
¿En qué medida la severidad actual del <strong>Trastorno por Déficit de Atención e Hiperactividad (TDAH)</strong> se explica por los <strong>síntomas en la infancia</strong>, la <strong>impulsividad objetiva</strong> y la <strong>ansiedad comórbida</strong> mediante Regresión Lineal Múltiple?
</div>

<div class="divider"></div>

<div class="meta">
<strong>Autores:</strong> Mariana Salazar · Luis Alejandro Luna Martínez<br>
<strong>Materia:</strong> Análisis de Regresión y Correlación (ARC) · <strong>Profesora:</strong> Cynthia Calderón García<br>
Dataset clínico <em>HYPERAKTIV</em> (Hicks et al., 2021) · 26 de noviembre de 2026<br>
<span style="font-size: 0.85em;"><em>Siglas:</em> <code>ASRS</code> (<em>Adult ADHD Self-Report Scale</em>).</span>
</div>

<!--
MARIANA (~1 min):
- El TDAH inicia en la infancia y suele persistir en la adultez.
- Evaluarlo en adultos es complejo porque depende mucho del autorreporte.
- Dataset clínico HYPERAKTIV (Hicks et al., 2021).
- Pregunta: ¿Cuánto de la severidad actual (ASRS) se explica por síntomas infantiles (WURS), impulsividad objetiva (CPT-II) y ansiedad (HADS_A)?
-->

---

<div class="speaker-tag">Parte 1 · Mariana</div>

## 1. ¿Por qué Regresión Lineal Múltiple y CRISP-ML(Q)?

<div class="grid-2" style="margin-top: 8px;">
  <div class="card card-navy">
    <strong>Corte transversal (no series de tiempo)</strong>
    <p style="font-size: 0.78em; margin: 8px 0 0 0; color: #475569;">
      Cada fila representa un paciente único evaluado en una sola sesión clínica, sin orden cronológico ni mediciones repetidas.
    </p>
  </div>
  <div class="card card-accent">
    <strong>Validez estadística</strong>
    <p style="font-size: 0.78em; margin: 8px 0 0 0; color: #475569;">
      Múltiples predictores lineales, muestra efectiva <code>n = 69 ≥ 30</code> e independencia confirmada (<code>Durbin-Watson = 2.174</code>).
    </p>
  </div>
</div>

<div class="flow">
  <div class="flow-step">1. Comprensión</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">2. Preparación</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">3. Modelado</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">4. Evaluación</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">5. Inferencia</div>
  <div class="flow-arrow">→</div>
  <div class="flow-step">6. Comunicación</div>
</div>

<div class="note-bar">
  <strong>Flujo reproducible:</strong> 4 cuadernos Jupyter secuenciales (<code>01</code> a <code>04</code>) en Python 3.13 + <code>uv</code> siguiendo el marco <strong>CRISP-ML(Q)</strong>.
</div>
<div class="siglas">
  <strong>Siglas:</strong> <code>CRISP-ML(Q)</code>: <em>Cross-Industry Standard Process for Machine Learning with Quality Assurance</em>.
</div>

<!--
MARIANA (~1 min):
- Corte transversal (no series de tiempo): cada fila es un paciente único evaluado una sola vez, sin orden temporal.
- Requisitos cumplidos: más de 2 predictores, n = 69 >= 30 y Durbin-Watson = 2.174 (sin autocorrelación).
- Metodología CRISP-ML(Q): flujo reproducible en 4 notebooks (01 a 04).
-->

---

<div class="speaker-tag">Parte 1 · Mariana</div>

## 2. Variables Clínicas y Control de Fuga de Datos

| Rol | Variable | Instrumento | Qué mide y escala |
| :---: | :--- | :--- | :--- |
| **$Y$** | **`ASRS`** | *Adult ADHD Self-Report Scale* (OMS) | Severidad actual autorreportada (`0–72`, 18 ítems DSM) |
| **$X_1$** | **`WURS`** | *Wender Utah Rating Scale* | Síntomas retrospectivos en la infancia (`0–100`, corte `≥ 46`) |
| **$X_2$** | **`Commissions`** | *Conners' CPT-II* (`General TScore`) | Impulsividad objetiva en prueba computarizada (`T > 60` elevado) |
| **$X_3$** | **`HADS_A`** | *Hospital Anxiety & Depression Scale* | Ansiedad comórbida (`0–21`, `≥ 11` clínicamente significativa) |

<div class="note-bar amber">
  <strong>Prevención de fuga de información (<em>data leakage</em>):</strong> Se excluyeron explícitamente <code>ID</code> y los diagnósticos binarios directos <code>ADHD</code> y <code>ADD</code>, ya que equivalen al diagnóstico mismo.
</div>
<div class="siglas">
  <strong>Siglas:</strong> <code>OMS</code>: Organización Mundial de la Salud · <code>DSM</code>: <em>Diagnostic and Statistical Manual of Mental Disorders</em> · <code>CPT-II</code>: <em>Conners' Continuous Performance Test II</em> · <code>HADS_A</code>: <em>Hospital Anxiety and Depression Scale – Anxiety</em> · <code>ADHD/ADD</code>: <em>Attention-Deficit/(Hyperactivity) Disorder</em>.
</div>

<!--
MARIANA (~1.5 min):
- Y (ASRS): escala OMS de severidad actual (0-72, 18 ítems DSM). Mayor puntaje = mayor severidad.
- 3 dimensiones complementarias:
  * X1 WURS (0-100): síntomas retrospectivos en infancia (corte orientativo >= 46).
  * X2 Commissions (puntaje T): impulsividad objetiva en prueba computarizada CPT-II (T > 60 elevado).
  * X3 HADS_A (0-21): ansiedad comórbida (>= 11 clínica).
- Control de fuga de datos: excluimos ID, ADHD y ADD porque equivalen al diagnóstico mismo.
-->

---

<div class="speaker-tag">Parte 1 · Mariana</div>

## 3. EDA: Distribución de `ASRS` y Correlaciones ($r$)

<div class="grid-2-asym">
  <div class="fig-wrap">
    <img src="../figures/asrs_distribucion.png" alt="Distribución de ASRS">
  </div>
  <div>
    <table>
      <thead><tr><th>Variable candidata</th><th><i>r</i></th><th><i>p</i>-valor</th></tr></thead>
      <tbody>
        <tr class="hl"><td><code>WURS</code></td><td>0.685</td><td>&lt; 0.001</td></tr>
        <tr class="hl"><td><code>Commissions</code></td><td>0.526</td><td>&lt; 0.001</td></tr>
        <tr><td><code>DPrime</code></td><td>0.398</td><td>&lt; 0.001</td></tr>
        <tr class="hl"><td><code>HADS_A</code></td><td>0.304</td><td>0.011</td></tr>
        <tr class="muted-row"><td><code>MADRS</code></td><td>0.171</td><td>0.154</td></tr>
        <tr class="muted-row"><td><code>HADS_D</code></td><td>0.112</td><td>0.361</td></tr>
        <tr class="muted-row"><td><code>AGE</code></td><td>−0.116</td><td>0.320</td></tr>
      </tbody>
    </table>
    <div class="note-bar" style="margin-top: 12px;">
      <strong><i>n</i> = 75 integrados:</strong> Media <code>41.4</code>, Mediana <code>42.0</code>, sin valores atípicos (ligera cola izquierda de 3 pacientes).
    </div>
    <div class="siglas">
      <strong>Siglas:</strong> <code>EDA</code>: Análisis Exploratorio de Datos · <code>MADRS</code>: <em>Montgomery–Åsberg Depression Rating Scale</em> · <code>HADS_D</code>: <em>HADS – Depression</em> · <code>AGE</code>: Edad.
    </div>
  </div>
</div>

<!--
MARIANA (~1.5 min):
- Señalar gráfica (izq.): n = 75, media 41.4, mediana 42.0, distribución simétrica y sin atípicos (ligera cola izquierda de 3 pacientes).
- Señalar tabla (der.):
  * WURS (r = 0.685, p < 0.001): correlación fuerte.
  * Commissions (r = 0.526, p < 0.001): prueba objetiva conectada con autorreporte.
  * HADS_A (r = 0.304, p = 0.011): significativa débil-moderada.
  * MADRS, HADS_D y AGE: no significativas (p > 0.15).
-->

---

<div class="speaker-tag">Parte 1 · Mariana</div>

## 4. Gráficas de Dispersión y Descarte de Candidatas

<div class="grid-2-asym">
  <div class="fig-wrap">
    <img src="../figures/dispersion_candidatas.png" alt="Dispersión de candidatas">
  </div>
  <div style="display: flex; flex-direction: column; gap: 14px;">
    <div class="card card-accent">
      <strong>Descarte de <code>Omissions</code> (<i>r</i> = 0.287)</strong>
      <p style="font-size: 0.72em; margin: 6px 0 0 0; color: #475569;">
        Un único punto influyente (<code>≈ 330</code>) jalaba artificialmente la recta de ajuste; sin él, la relación lineal desaparece.
      </p>
    </div>
    <div class="card card-navy">
      <strong>Descarte de <code>DPrime</code> (<i>r</i> = 0.398)</strong>
      <p style="font-size: 0.72em; margin: 6px 0 0 0; color: #475569;">
        Alta colinealidad con <code>Commissions</code> (<code>r = 0.88</code>); ambas miden discriminación/impulsividad en el mismo test <code>CPT-II</code> (<em>Conners' Continuous Performance Test II</em>).
      </p>
    </div>
  </div>
</div>

<!--
MARIANA (~1 min):
- Regla clave: siempre graficar, no confiar solo en r.
- Omissions (r = 0.287) descartada: un solo paciente extremo (~330) jalaba la recta; sin él, la relación desaparece.
- DPrime (r = 0.398) descartada: alta colinealidad con Commissions (r = 0.88) dentro del mismo test CPT-II.
-->

---

<div class="speaker-tag">Parte 1 · Mariana → Transición a Richie</div>

## 5. Impacto Clínico: Peso por +1 Desviación Estándar

<p style="font-size: 0.78em; color: #475569; margin: 0 0 12px 0;">
  Como cada escala tiene unidades distintas, comparamos el cambio esperado en <code>ASRS</code> al aumentar <strong>+1 DE muestral</strong> de cada predictor (<em>ceteris paribus</em>):
</p>

<div class="grid-3">
  <div class="kpi-card amber">
    <div class="kpi-val">+7.7 pts</div>
    <div class="kpi-title"><code>WURS</code> (<i>X</i><sub>1</sub>)</div>
    <div class="kpi-desc">Pesa el doble que <code>Commissions</code>; principal impulsor de severidad.</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-val">+3.8 pts</div>
    <div class="kpi-title"><code>Commissions</code> (<i>X</i><sub>2</sub>)</div>
    <div class="kpi-desc">La prueba objetiva aporta señal clínica independiente.</div>
  </div>
  <div class="kpi-card muted">
    <div class="kpi-val">+0.6 pts</div>
    <div class="kpi-title"><code>HADS_A</code> (<i>X</i><sub>3</sub>)</div>
    <div class="kpi-desc">Efecto marginal al controlar por historia infantil.</div>
  </div>
</div>

<div class="note-bar" style="margin-top: 22px;">
  <strong>Interpretación clínica:</strong> Quien reporta mayor carga sintomática desde la infancia y mayor desinhibición objetiva tiende a presentar puntuaciones más altas de <code>ASRS</code>.
</div>
<div class="siglas">
  <strong>Siglas:</strong> <code>DE</code>: Desviación Estándar · <code>WURS</code>: <em>Wender Utah Rating Scale</em> · <code>HADS_A</code>: <em>Hospital Anxiety and Depression Scale – Anxiety</em>.
</div>

<!--
MARIANA (~1 min):
- Como las escalas son distintas, comparamos el efecto de +1 DE muestral (ceteris paribus):
  * WURS: +7.7 pts de ASRS (pesa el doble que Commissions).
  * Commissions: +3.8 pts (aporta señal objetiva independiente).
  * HADS_A: +0.6 pts (efecto marginal al controlar por las otras dos).
- Transición: ceder la palabra a Richie.
-->

---

<div class="speaker-tag">Parte 2 · Richie</div>

## 6. Ingeniería de Datos y Validación por `VIF`

<div class="grid-2" style="align-items: start; margin-top: 8px;">
  <div class="card card-navy">
    <strong>Protocolo de Calidad e Integración</strong>
    <ul style="font-size: 0.74em; margin: 10px 0 0 0; padding-left: 20px; color: #334155;">
      <li>Cruce (<em>inner join</em>) de 3 CSVs por <code>ID</code> (<code>sep=";"</code>, <code>utf-8-sig</code>).</li>
      <li>Filtro CPT-II: <code>Raw Score Omissions &lt; 300</code>.</li>
      <li>Depuración de 885 columnas → <strong><i>n</i> = 75</strong> integrados.</li>
      <li>Casos completos: 1 nulo en <code>WURS</code>, 6 en <code>HADS_A</code> → <strong><i>n</i> = 69</strong>.</li>
    </ul>
  </div>
  <div>
    <table>
      <thead><tr><th>Predictor</th><th><code>VIF</code></th><th>Diagnóstico</th></tr></thead>
      <tbody>
        <tr><td><code>WURS</code></td><td><strong>1.623</strong></td><td>Sin colinealidad</td></tr>
        <tr><td><code>Commissions</code></td><td><strong>1.390</strong></td><td>Sin colinealidad</td></tr>
        <tr><td><code>HADS_A</code></td><td><strong>1.205</strong></td><td>Sin colinealidad</td></tr>
      </tbody>
    </table>
    <div class="formula-box" style="margin-top: 14px; font-size: 0.80em;">

$$\text{VIF}_j = \frac{1}{1 - R_j^2} < 2 \quad (\text{umbral clásico } < 5)$$

</div>
  </div>
</div>
<div class="siglas">
  <strong>Siglas:</strong> <code>VIF</code>: <em>Variance Inflation Factor</em> (Factor de Inflación de la Varianza) · <code>CSV</code>: <em>Comma-Separated Values</em> · <code>CPT-II</code>: <em>Conners' Continuous Performance Test II</em>.
</div>

<!--
RICHIE (~1.5 min):
- Integración: inner join de 3 CSVs por ID (sep=";", utf-8-sig).
- Filtro de calidad CPT-II: Raw Score Omissions < 300 para descartar sesiones inválidas.
- Depuración: 885 columnas -> n = 75 integrados -> n = 69 casos completos (1 nulo en WURS, 6 en HADS_A).
- Multicolinealidad (VIF): WURS = 1.623, Commissions = 1.390, HADS_A = 1.205 (todos < 2, umbral < 5).
-->

---

<div class="speaker-tag">Parte 2 · Richie</div>

## 7. Modelo MCO Estimado, Bondad de Ajuste y Pruebas $F$ / $t$

<div class="formula-box">

$$\widehat{\text{ASRS}}_i = 7.6350 + 0.3678\,\text{WURS}_i + 0.3079\,\text{Commissions}_i + 0.1273\,\text{HADS\_A}_i$$

</div>

<div class="grid-3">
  <div class="kpi-card">
    <div class="kpi-val">53.41 %</div>
    <div class="kpi-title"><i>R</i><sup>2</sup> (<i>R</i><sup>2</sup><sub>adj</sub> = 0.5126)</div>
    <div class="kpi-desc"><code>RMSE = 9.90</code> puntos de <code>ASRS</code></div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-val">24.84</div>
    <div class="kpi-title">Prueba <i>F</i>(3, 65)</div>
    <div class="kpi-desc"><code>p = 8.00e-11</code> (globalmente significativo)</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-val" style="font-size: 1.35em; padding-top: 8px;">2 / 3 sig.</div>
    <div class="kpi-title">Pruebas <i>t</i> individuales</div>
    <div class="kpi-desc"><code>WURS</code> (<code>p&lt;0.001</code>), <code>Commissions</code> (<code>p=0.010</code>)<br><code>HADS_A</code> (<code>p=0.655</code>), <code>const</code> (<code>p=0.216</code>)</div>
  </div>
</div>
<div class="siglas" style="margin-top: 16px;">
  <strong>Siglas:</strong> <code>MCO</code>: Mínimos Cuadrados Ordinarios · <code>RMSE</code>: <em>Root Mean Squared Error</em> (Raíz del Error Cuadrático Medio) · <code>R<sup>2</sup><sub>adj</sub></code>: R² ajustado.
</div>

<!--
RICHIE (~1.5 min):
- Ecuación: ASRS = 7.6350 + 0.3678*WURS + 0.3079*Commissions + 0.1273*HADS_A.
- Ajuste global: R^2 = 53.41 % (R^2_adj = 0.5126), RMSE = 9.90.
- Prueba F(3, 65) = 24.84 (p = 8.00e-11, altamente significativo).
- Pruebas t: WURS (p < 0.001) y Commissions (p = 0.010) significativos; HADS_A (p = 0.655) y const (p = 0.216) no significativos.
-->

---

<div class="speaker-tag">Parte 2 · Richie</div>

## 8. Ajuste Real vs. Predicho y Diagnóstico de Residuales

<div class="grid-2">
  <div class="fig-wrap">
    <img src="../figures/ols_real_vs_predicho.png" alt="Real vs Predicho">
  </div>
  <div class="fig-wrap">
    <img src="../figures/ols_residual_diagnostics.png" alt="Diagnóstico de Residuales">
  </div>
</div>

<div class="note-bar" style="text-align: center; font-size: 0.72em;">
  <strong>Supuestos cumplidos (<i>α</i> = 0.05):</strong>
  Normalidad Shapiro-Wilk <code>p = 0.2634</code> (✓) ·
  Homocedasticidad Breusch-Pagan <code>p = 0.0796</code> (✓) ·
  Independencia <code>DW = 2.174</code> (✓) ·
  Cook <code>0 casos &gt; 1</code> (✓)
</div>
<div class="siglas" style="text-align: center;">
  <strong>Siglas:</strong> <code>DW</code>: Estadístico de Durbin-Watson (prueba de autocorrelación).
</div>

<!--
RICHIE (~1.5 min):
- Real vs. predicho (izq.): puntos alineados a la diagonal identidad sin curvaturas.
- Supuestos cumplidos (alfa = 0.05):
  * Normalidad: Shapiro-Wilk p = 0.2634 (OK).
  * Homocedasticidad: Breusch-Pagan p = 0.0796 (OK, cerca del 5 %).
  * Independencia: DW = 2.174 (OK).
  * Influyentes: Cook 0 casos > 1 (OK).
- Ese p = 0.0796 y el p de HADS_A motivaron probar transformaciones.
-->

---

<div class="speaker-tag">Parte 2 · Richie</div>

## 9. Transformaciones y Reversión a Escala Original

| Modelo evaluado | `RMSE` (escala `ASRS`) | Shapiro-Wilk $p$ | Breusch-Pagan $p$ | Veredicto |
| :--- | :---: | :---: | :---: | :--- |
| **Base lineal** | **9.61** | **0.263** (✓) | **0.080** (✓) | **Elegido (cumple todo)** |
| $\ln(\text{ASRS})$ | 10.51 | `&lt; 0.001` (✗) | `0.027` (✗) | Estira cola izquierda |
| $\sqrt{\text{ASRS}}$ | 9.73 | `0.013` (✗) | `0.022` (✗) | Rompe normalidad |
| Parsimonioso (sin `HADS_A`) | 9.63 | `0.283` (✓) | `0.041` (✗) | Rompe homocedasticidad |

<div class="grid-2" style="margin-top: 14px;">
  <div class="formula-box" style="margin: 0; font-size: 0.75em;">

Reversión: $\widehat{\text{ASRS}} = e^{\hat z + \hat\sigma^2/2}$ &nbsp;y&nbsp; $\widehat{\text{ASRS}} = \hat z^2 + \hat\sigma^2$

  </div>
  <div class="note-bar amber" style="margin: 0;">
    <strong>Conclusión metodológica:</strong> El modelo lineal base es el único que preserva todos los supuestos y minimiza el error.
  </div>
</div>
<div class="siglas">
  <strong>Siglas:</strong> <code>RMSE</code>: <em>Root Mean Squared Error</em> · <code>ASRS</code>: <em>Adult ADHD Self-Report Scale</em> · <code>HADS_A</code>: <em>Hospital Anxiety and Depression Scale – Anxiety</em>.
</div>

<!--
RICHIE (~1.5 min):
- Comparación justa: se revirtieron ln(ASRS) y sqrt(ASRS) a escala original (e^(z + sigma^2/2) y z^2 + sigma^2).
- ln(ASRS) y sqrt(ASRS): estiran la cola izquierda, rompen normalidad (p < 0.001 y 0.013), empeoran homocedasticidad y suben el RMSE.
- Sin HADS_A: sube ligeramente R^2_adj, pero rompe homocedasticidad (p = 0.041 < 0.05).
- Decisión: el modelo lineal base es el único que cumple todos los supuestos y minimiza el error (RMSE = 9.61).
-->

---

<div class="speaker-tag">Parte 2 · Richie & Cierre Conjunto</div>

<h2 style="margin-bottom: 12px;">10. Pronósticos en 3 Perfiles Clínicos y Conclusión</h2>

<div class="grid-2-asym" style="grid-template-columns: 0.92fr 1.08fr; gap: 18px; align-items: center;">
  <div class="fig-wrap" style="padding: 6px;">
    <img src="../figures/ols_forecasts_profiles.png" alt="Pronósticos por perfil" style="max-height: 235px;">
  </div>
  <div>
    <table style="font-size: 0.54em;">
      <thead><tr><th>Perfil</th><th>Pred.</th><th>IC 95 %</th><th>IP 95 %</th></tr></thead>
      <tbody>
        <tr><td><strong>Baja (P10)</strong></td><td><strong>27.14</strong></td><td>[22.48, 31.81]</td><td>[6.82, 47.46]</td></tr>
        <tr><td><strong>Mod. (P50)</strong></td><td><strong>40.31</strong></td><td>[37.90, 42.72]</td><td>[20.39, 60.23]</td></tr>
        <tr class="hl"><td><strong>Alta (P90)</strong></td><td><strong>56.06</strong></td><td>[51.11, 61.00]</td><td>[35.67, 72.00]*</td></tr>
      </tbody>
    </table>
    <div style="font-size: 0.46em; color: #64748B; margin-top: 5px;">*Límite estadístico superior 76.44 acotado al máximo clínico (72).</div>
    <div class="siglas" style="margin-top: 6px;">
      <strong>Siglas:</strong> <code>P10/P50/P90</code>: Percentiles 10, 50 y 90 · <code>IC</code>: Intervalo de Confianza · <code>IP</code>: Intervalo de Predicción.
    </div>
  </div>
</div>

<div class="card card-accent" style="padding: 8px 14px; margin-top: 8px;">
  <div style="font-size: 0.58em; margin: 0; line-height: 1.32; color: #1E293B;">
    <strong>Cierre clínico:</strong> Brecha clara de <strong>28.9 puntos</strong> útil para <strong>cribado y estratificación</strong>, pero el IP individual de <code>±20 pts</code> confirma que <strong>complementa y no sustituye</strong> la entrevista clínica.
  </div>
</div>

<!--
RICHIE & MARIANA (~1.5 min):
- Sin extrapolación: perfiles basados en percentiles P10, P50 y P90 de la muestra (n = 69):
  * Carga baja (P10): 27.14 (IC [22.48, 31.81], IP [6.82, 47.46]).
  * Carga moderada (P50): 40.31 (IC [37.90, 42.72], IP [20.39, 60.23]).
  * Carga alta (P90): 56.06 (IC [51.11, 61.00], IP [35.67, 72.00] acotado al máximo clínico 72).
- Cierre conjunto:
  * Brecha de 28.9 puntos útil para cribado y estratificación.
  * IP individual de +-20 puntos (~47 % varianza no explicada) -> complementa, no sustituye la entrevista clínica.
-->

---

<!-- _class: lead -->
<!-- _paginate: false -->

<div class="badge">Fin de la Presentación</div>

# ¡Muchas Gracias por su Atención!

<div class="subtitle" style="font-size: 1.05em;">
¿Preguntas o comentarios?
</div>

<div class="divider"></div>

<div class="meta">
<strong>Mariana Salazar · Luis Alejandro Luna Martínez</strong><br>
Análisis de Regresión y Correlación (ARC) · Universidad Autónoma de Baja California (UABC)<br>
<em>Código y reporte reproducible:</em> <code>github.com/a1252765/ARC_project</code>
</div>

<!--
Agradecer y abrir ronda de preguntas.

BANCO RÁPIDO DE Q&A:
- ¿Por qué dejaron HADS_A si p = 0.655? Al quitarla se rechaza homocedasticidad (Breusch-Pagan p = 0.041 < 0.05); mantenerla preserva supuestos, baja el RMSE (9.61 vs 9.63) y controla ansiedad.
- ¿Por qué empeoró ln(ASRS)? ASRS tenía ligera cola izquierda (3 pacientes 6-10); ln separó esos bajos y destruyó normalidad (p < 0.001).
- ¿Cómo evitaron extrapolación? Usando percentiles observados P10, P50 y P90 de n = 69.
- ¿Por qué IP llega a 76.44 en Carga Alta? MCO asume respuesta no acotada; reportamos el valor estadístico (76.44) y el acotado al dominio clínico (72.00).
-->
