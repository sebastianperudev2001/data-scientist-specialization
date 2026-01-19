# Análisis de Estrategias de Datos - ENAHO SALUD

Este documento describe la lógica y el planteamiento de análisis de datos utilizado en el notebook `DMC_DS19_TareaFinal_ENAHO_SALUD.ipynb`. El objetivo es servir como guía para orientar tu propio análisis exploratorio.

## 1. Definición de Objetivos

El análisis aborda dos problemas principales:

1.  **Clasificación (Target: `P401`)**: Predecir si una persona padece alguna enfermedad o malestar crónico.
2.  **Regresión (Target: `GASTO TOTAL`)**: Predecir/Explicar el gasto total en salud basado en variables demográficas (específicamente la edad).

## 2. Preprocesamiento y Limpieza de Datos

La limpieza es rigurosa y sigue una lógica de negocio clara:

- **Selección de Variables**: Se filtran inicialmente solo las columnas relevantes (`GASTO TOTAL`, `AREA`, `P208A` (Edad), `P207` (Sexo), `P301A` (Nivel Educativo), etc.) para reducir el ruido.
- **Manejo de Nulos Críticos**:
  - Se eliminan registros donde el target (`P401`) es nulo, asumiendo que si no se respondió la pregunta clave, el registro no es útil.
  - Se eliminan registros sin `NIVEL`, correlacionándolo con la falta de tipo de cuestionario.
- **Tratamiento de Outliers (Valores Atípicos)**:
  - **Gasto Total**: Se eliminan gastos mayores a 2500, considerándolos errores de digitación (posible confusión de decimales en tablets).
  - **Edad (`P208A`)**: Se definen límites lógicos (mínimo 21 años, máximo calculado por rango intercuartil - IQR) para el conjunto de entrenamiento, evitando que edades extremas sesguen el modelo.
- **Creación de Nuevas Variables (Feature Extraction)**:
  - **Discapacidad**: Se crea una variable binaria sintetizando múltiples columnas (`P401H1` a `P401H6`). Si alguna tiene "Si", se marca como discapacidad. Esto reduce dimensionalidad y crea una variable más potente.

## 3. Ingeniería de Características (Feature Engineering)

El notebook aplica transformaciones avanzadas para preparar los datos para los modelos:

- **Imputación de Valores Faltantes**:
  - **Estado Civil (`P209`)**: Se asume "Casado(a)" para los valores nulos (moda/lógica de negocio).
  - **Nivel Educativo (`P301A`)**: Los nulos se llenan con "Secundaria Completa" (moda en el set de test) y los códigos '99' se etiquetan como "Sin Nivel".
- **Codificación (Encoding)**:
  - Se transforman variables categóricas (Texto) a Numéricas manualmente mediante `map`.
    - _Ejemplo_: Sexo (Hombre=0, Mujer=1), Área (Urbano=0, Rural=1), Estado Civil, Nivel Educativo (con una escala ordinal no lineal).
- **Weight of Evidence (WoE)**:
  - Utilizan la técnica de **WoE** (Peso de la Evidencia) usando la librería `optbinning` para transformar variables categóricas según su poder predictivo respecto al target binario (`P401`). Esto linealiza relaciones no lineales en variables categóricas.

## 4. Análisis Exploratorio (EDA) y Visualización

Se utilizan gráficos para validar hipótesis antes de modelar:

- **Distribuciones**: Histogramas y Boxplots para ver la dispersión de la Edad y el Gasto, identificando sesgos y outliers.
- **Correlaciones**: `Pairplot` y `Heatmap` de correlación para ver relaciones entre variables numéricas.
- **Análisis Bivariado**: `lmplot` (Scatterplot con línea de regresión) para visualizar la relación lineal entre Edad y Gasto, segmentando por Nivel Educativo o Enfermedad Crónica.

## 5. Estrategias de Modelado

### A. Regresión Logística (Modelo Clasificatorio)

- **Objetivo**: Predecir enfermedad crónica (`P401`).
- **Estrategia**: Usar variables transformadas (algunas con WoE, otras con one-hot/ordinal encoding) para entrenar un modelo lineal que clasifique la probabilidad de enfermedad.

### B. Regresión Lineal (Modelo Predictivo/Explicativo)

- **Objetivo**: Explicar el `GASTO TOTAL`.
- **Variable Predictora Principal**: Edad (`P208A`).
- **Herramientas**: `statsmodels` (OLS) para interpretación estadística y `sklearn` para predicción.
- **Validación**:
  - **P-valor**: Se revisa si la Edad es estadísticamente significativa (< 0.05).
  - **Análisis de Residuos**: Se grafican residuos vs. valores predichos para verificar si el error es aleatorio o si hay patrones no capturados.
  - **Métricas**: MSE (Error Cuadrático Medio) y R2 (Coeficiente de Determinación).

## Recomendaciones para tu Análisis

Basado en este notebook, te sugiero seguir estos pasos:

1.  **Limpieza Inteligente**: No elimines nulos a ciegas. Analiza si la ausencia de dato tiene un significado (ej. no aplica, no respondió por X razón) e imputa usando la moda o medias lógicas.
2.  **Crea Variables**: Busca agrupar columnas relacionadas (como hicieron con Discapacidad) para simplificar tu dataset.
3.  **Visualiza antes de Modelar**: Usa Boxplots para decidir qué es un outlier y Scatterplots para ver si vale la pena una regresión lineal.
4.  **Divide tu Análisis**: Separa variables categóricas de numéricas y trátalas diferente (Encoding vs Normalización/Scaling).
