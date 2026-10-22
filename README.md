# Titanic Dataset — Data Mining, Preprocessing & Exploratory Analysis

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![Libraries](https://img.shields.io/badge/Libraries-Pandas%20%7C%20Seaborn%20%7C%20Matplotlib%20%7C%20NumPy-green.svg)](#dependencies)
[![Assignment](https://img.shields.io/badge/Course-Data%20Mining-purple.svg)](#overview)

A complete, end-to-end data mining project covering **data cleaning, missing value imputation, outlier detection, feature engineering, and statistical visualization** on the benchmark **Titanic Passenger Survival Dataset**.

This repository contains reproducible scripts, an interactive Jupyter Notebook, publication-grade figures, and an automated assignment report generator.

---

## Project Overview

* **Domain:** Data Mining / Exploratory Data Analysis (EDA) / Statistical Preprocessing
* **Dataset:** Titanic Passenger Survival Dataset (891 passenger records, 15 initial attributes)
* **Target Analytical Goal:** Identify social, demographic, and economic factors influencing passenger survival during the 1912 Titanic disaster through rigorous exploratory mining techniques.

---

## Mining & Preprocessing Workflow

1. **Schema & Quality Inspection:**
   - Evaluated 6 numerical, 7 categorical, and 2 boolean attributes.
   - Identified missingness patterns across `age` (19.9%), `cabin`/`deck` (77.1%), and `embarked` (0.2%).

2. **Cleaning & Missing Value Imputation:**
   - **`age`**: Imputed using median age grouped by passenger class (`pclass`) and sex (`sex`) to preserve demographic integrity.
   - **`embarked` / `embark_town`**: Imputed using the modal embarkation port (Southampton, `S`).
   - **`deck`**: Transformed into a missingness indicator category (`Unknown`) rather than dropping records, preserving 77% of rows.
   - **Deduplication**: Audited and confirmed zero duplicate records.

3. **Outlier Detection & Handling:**
   - Explored fare skewness and detected extreme upper-tail outliers using the Interquartile Range (IQR) rule ($Q_3 + 1.5 \times \text{IQR}$).
   - Applied soft upper-quantile capping (winsorization) to avoid model distortion while retaining variance.

4. **Feature Engineering & Transformation:**
   - Extracted `family_size = sibsp + parch + 1` and derived `is_alone`.
   - Normalization and categorical encoding ready for downstream predictive modeling.

---

## Visualizations & Key Findings

| Figure | Type | Key Insight |
| :--- | :--- | :--- |
| **Figure 0** | Missing Values Plot | Highlights critical missing rates in `deck` (688) and `age` (177). |
| **Figure 1** | Bar Chart | 1st class passengers survived at ~63%, compared to only ~24% for 3rd class. |
| **Figure 2** | Histogram & KDE | Children (ages 0–10) experienced the highest survival rates; working-age adults suffered high mortality. |
| **Figure 3** | Box Plot | Clear economic stratification: 1st class fares exhibit heavy right-skew and higher median ticket costs. |
| **Figure 4** | Scatter Plot | High-fare passengers and younger individuals concentrate heavily in the survived cluster. |
| **Figure 5** | Correlation Heatmap | Strongest survival predictors: Fare ($+0.26$) and Pclass ($-0.34$). |

*All rendered high-resolution plots are available in the [`figures/`](figures/) directory.*

---

## 📁 Repository Structure

```text
├── Assignment1_Data_Mining.ipynb       # Fully executed Jupyter Notebook with annotations
├── Assignment1_Data_Mining_Report.docx  # Comprehensive academic assignment report (Word)
├── titanic_dataset.csv                 # Raw Titanic passenger dataset (891 rows)
├── titanic_cleaned.csv                 # Preprocessed & cleaned dataset
├── build_notebook.py                   # Programmatic notebook constructor
├── generate_visuals.py                 # Generates publication-grade figures (figures/*.png)
├── execute_notebook.py                 # Headless Jupyter notebook runner
├── create_word_report.py               # Generates the formatted Word (.docx) report
├── figures/                            # High-DPI rendered visual figures
│   ├── figure0_missing_values.png
│   ├── figure1_bar_chart.png
│   ├── figure2_histogram.png
│   ├── figure3_box_plot.png
│   ├── figure4_scatter_plot.png
│   └── figure5_correlation_heatmap.png
├── .gitignore                          # Standard git ignore rules
└── README.md                           # Project documentation
```

---

## Getting Started & Reproduction

### 1. Prerequisites
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Fetoooo/titanic-eda-data-mining.git
cd titanic-eda-data-mining
pip install pandas numpy matplotlib seaborn jupyter python-docx nbformat
```

### 2. Re-generating Figures & Preprocessed Data
Run the visualization and cleaning pipeline:
```bash
python generate_visuals.py
```

### 3. Rebuilding the Jupyter Notebook
```bash
python build_notebook.py
python execute_notebook.py
```

### 4. Rebuilding the Word Report
```bash
python create_word_report.py
```

---

## Author
* **Name:** Fathy Ayman Fathy
* **Course:** Data Mining (26/27) — Section 3
