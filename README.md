# Proyecto Final — Análisis de Regresión y Correlación (ARC)

Modelado de la severidad de síntomas de TDAH en adultos (`ASRS`) en el dataset clínico **HYPERAKTIV** (Hicks et al., 2021) mediante **Regresión Lineal Múltiple por Mínimos Cuadrados Ordinarios (MCO)**.

## Equipo y Roles

* **Richie:** Ingeniería de datos, modelado MCO (`statsmodels`), diagnóstico de supuestos, pronósticos y ensamblaje técnico.
* **Mariana:** Análisis exploratorio (EDA), interpretación clínica/estadística, redacción del reporte (Obsidian Markdown + LaTeX $\rightarrow$ PDF) y coordinación de entregables.

## Fechas Clave

* **Jueves 19 de noviembre:** Registro de equipo y base de datos con el profesor.
* **Miércoles 25 de noviembre (11:59 p.m.):** Entrega del reporte final en PDF (Classroom).
* **Jueves 26 de noviembre:** Exposición oral (12–15 min).

---

## Configuración Inicial en Ubuntu con `uv`

### 1. Instalar `uv` (si no está instalado)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Reinicia la terminal o ejecuta `source ~/.local/bin/env`.

### 2. Clonar el repositorio y sincronizar dependencias
```bash
git clone <URL_DEL_REPO_EN_GITHUB>
cd ARC_project
uv sync
```

### 3. Colocar los datos (Google Drive)
Descarga los 3 archivos CSV desde la carpeta compartida de Google Drive y colócalos en `data/raw/`:
* `data/raw/patient_info.csv`
* `data/raw/features.csv`
* `data/raw/CPT_II_ConnersContinuousPerformanceTest.csv`

*(Los archivos `.csv` están en `.gitignore` para no subir el dataset al repositorio).*

### 4. Ejecutar el pipeline de preparación y EDA inicial
```bash
uv run python scripts/run_pipeline.py
```

---

## Flujo de Trabajo en GitHub (2 Personas)

1. Crear una rama para tu tarea desde `main` actualizado:
   ```bash
   git checkout main && git pull
   git checkout -b feature/nombre-tarea
   ```
2. Si agregas una librería nueva, usa siempre `uv add <paquete>` y sube los cambios de `pyproject.toml` y `uv.lock`. El otro integrante solo ejecuta `uv sync`.
3. Mantener la lógica reutilizable en `src/arc_project/` y usar `notebooks/` para exploración y generación de figuras.
4. Abrir un Pull Request hacia `main` antes de fusionar.
