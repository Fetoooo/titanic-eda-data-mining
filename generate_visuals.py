import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

os.makedirs('figures', exist_ok=True)

# -------------------------------------------------------------
# Part 1: Dataset Loading
# -------------------------------------------------------------
print("--- Part 1: Loading Dataset ---")
df_raw = pd.read_csv('titanic_dataset.csv')
print(f"Raw dataset shape: {df_raw.shape}")

# -------------------------------------------------------------
# Part 2: Exploration Visuals
# -------------------------------------------------------------
print("--- Part 2: Generating Exploration Visuals ---")
# Missing values plot
missing_counts = df_raw.isnull().sum()
missing_counts = missing_counts[missing_counts > 0].sort_values(ascending=False)

plt.figure(figsize=(8, 4.5))
bars = plt.bar(missing_counts.index, missing_counts.values, color=['#d9534f', '#f0ad4e', '#5bc0de', '#5cb85c'])
plt.title('Exploration: Missing Values Count per Feature in Raw Dataset', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Features with Missing Values', fontsize=12, fontweight='bold')
plt.ylabel('Number of Missing Records (out of 891)', fontsize=12, fontweight='bold')
for bar in bars:
    height = bar.get_height()
    pct = (height / len(df_raw)) * 100
    plt.annotate(f'{height}\n({pct:.1f}%)',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.ylim(0, 800)
plt.tight_layout()
plt.savefig('figures/figure0_missing_values.png', dpi=300)
plt.close()

# -------------------------------------------------------------
# Part 3: Data Cleaning & Preprocessing
# -------------------------------------------------------------
print("--- Part 3: Cleaning & Preprocessing ---")
df_clean = df_raw.copy()

# Step 1: Handling Missing Values
# Impute Age using median age by Pclass and Sex
median_ages = df_clean.groupby(['pclass', 'sex'])['age'].transform('median')
df_clean['age'] = df_clean['age'].fillna(median_ages)

# Impute Embarked and Embark_town using mode ('S' / 'Southampton')
mode_embarked = df_clean['embarked'].mode()[0]
mode_embark_town = df_clean['embark_town'].mode()[0]
df_clean['embarked'] = df_clean['embarked'].fillna(mode_embarked)
df_clean['embark_town'] = df_clean['embark_town'].fillna(mode_embark_town)

# Step 2: Drop redundant and excessively missing columns
# 'deck' has >77% missing; 'embark_town', 'alive', 'class', 'who', 'adult_male' are redundant
cols_to_drop = ['deck', 'embark_town', 'alive', 'class', 'who', 'adult_male']
df_clean.drop(columns=cols_to_drop, inplace=True)

# Step 3: Identify & Remove Duplicated Rows
dup_count_before = df_clean.duplicated().sum()
print(f"Duplicates before removal: {dup_count_before}")
df_clean.drop_duplicates(inplace=True)
df_clean.reset_index(drop=True, inplace=True)
print(f"Duplicates after removal: {df_clean.duplicated().sum()}")
print(f"Dataset shape after dropping duplicates: {df_clean.shape}")

# Step 4: Additional Preprocessing (Renaming and Data Types)
df_clean.rename(columns={
    'survived': 'Survived',
    'pclass': 'Passenger_Class',
    'sex': 'Gender',
    'age': 'Age',
    'sibsp': 'Siblings_Spouses',
    'parch': 'Parents_Children',
    'fare': 'Fare',
    'embarked': 'Embarkation_Port',
    'alone': 'Is_Alone'
}, inplace=True)

df_clean['Age'] = df_clean['Age'].round().astype(int)
df_clean['Is_Alone'] = df_clean['Is_Alone'].astype(int)

# Step 5: Convert Categorical to Numerical
# Gender: male -> 0, female -> 1
gender_map = {'male': 0, 'female': 1}
df_clean['Gender_Code'] = df_clean['Gender'].map(gender_map)

# Embarkation_Port: S -> 0, C -> 1, Q -> 2
port_map = {'S': 0, 'C': 1, 'Q': 2}
df_clean['Port_Code'] = df_clean['Embarkation_Port'].map(port_map)

df_clean.to_csv('titanic_cleaned.csv', index=False)
print("Saved titanic_cleaned.csv successfully!")

# -------------------------------------------------------------
# Part 5: Five Distinct Visualizations
# -------------------------------------------------------------
print("--- Part 5: Generating 5 Required Visualizations ---")

# Figure 1: Bar Chart
plt.figure(figsize=(8, 5))
bar_data = df_clean.groupby(['Passenger_Class', 'Gender'])['Survived'].mean().reset_index()
bar_data['Gender_Label'] = bar_data['Gender'].map({'female': 'Female', 'male': 'Male'})

palette = {'Female': '#e74c3c', 'Male': '#3498db'}
ax = sns.barplot(
    data=bar_data, 
    x='Passenger_Class', 
    y='Survived', 
    hue='Gender_Label', 
    palette=palette,
    edgecolor='black',
    linewidth=1.2
)
plt.title('Figure 1: Passenger Survival Rate by Travel Class and Gender', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Passenger Travel Class (1 = 1st Class, 2 = 2nd Class, 3 = 3rd Class)', fontsize=11, fontweight='bold')
plt.ylabel('Survival Rate (Proportion)', fontsize=11, fontweight='bold')
plt.ylim(0, 1.15)
plt.legend(title='Gender', title_fontsize='11', fontsize='10', loc='upper right')

for p in ax.patches:
    height = p.get_height()
    if not np.isnan(height) and height > 0:
        ax.annotate(f'{height*100:.1f}%',
                    xy=(p.get_x() + p.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/figure1_bar_chart.png', dpi=300)
plt.close()

# Figure 2: Histogram with KDE
plt.figure(figsize=(9, 5))
sns.histplot(
    data=df_clean,
    x='Age',
    hue='Survived',
    bins=30,
    kde=True,
    palette={0: '#e74c3c', 1: '#2ecc71'},
    multiple='layer',
    edgecolor='black',
    alpha=0.55
)
plt.title('Figure 2: Passenger Age Distribution by Survival Outcome (with KDE)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Passenger Age (Years)', fontsize=11, fontweight='bold')
plt.ylabel('Passenger Count', fontsize=11, fontweight='bold')
plt.legend(title='Survival Status', labels=['Survived (1)', 'Did Not Survive (0)'], loc='upper right')
plt.tight_layout()
plt.savefig('figures/figure2_histogram.png', dpi=300)
plt.close()

# Figure 3: Box Plot
plt.figure(figsize=(8, 5))
sns.boxplot(
    data=df_clean,
    x='Passenger_Class',
    y='Fare',
    palette=['#f1c40f', '#9b59b6', '#34495e'],
    boxprops=dict(alpha=0.85, edgecolor='black', linewidth=1.2),
    flierprops=dict(marker='o', markerfacecolor='#e74c3c', markersize=6, alpha=0.7)
)
plt.title('Figure 3: Ticket Fare Distribution Across Passenger Classes', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Passenger Travel Class', fontsize=11, fontweight='bold')
plt.ylabel('Ticket Fare ($ / £)', fontsize=11, fontweight='bold')
plt.yscale('log')
plt.tight_layout()
plt.savefig('figures/figure3_box_plot.png', dpi=300)
plt.close()

# Figure 4: Scatter Plot
plt.figure(figsize=(9, 5.5))
sns.scatterplot(
    data=df_clean,
    x='Age',
    y='Fare',
    hue='Survived',
    palette={0: '#e74c3c', 1: '#27ae60'},
    style='Survived',
    markers={0: 'X', 1: 'o'},
    s=75,
    alpha=0.75,
    edgecolor='w'
)
plt.title('Figure 4: Scatter Plot of Passenger Age vs. Ticket Fare by Survival Status', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Passenger Age (Years)', fontsize=11, fontweight='bold')
plt.ylabel('Ticket Fare ($ / £)', fontsize=11, fontweight='bold')
plt.legend(title='Outcome', labels=['Did Not Survive (0)', 'Survived (1)'], loc='upper right')
plt.tight_layout()
plt.savefig('figures/figure4_scatter_plot.png', dpi=300)
plt.close()

# Figure 5: Correlation Heatmap
plt.figure(figsize=(8.5, 6.5))
corr_cols = ['Survived', 'Passenger_Class', 'Gender_Code', 'Age', 'Siblings_Spouses', 'Parents_Children', 'Fare', 'Port_Code', 'Is_Alone']
corr_matrix = df_clean[corr_cols].corr()

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix, 
    annot=True, 
    fmt='.2f', 
    cmap='vlag', 
    vmin=-0.6, 
    vmax=0.6, 
    center=0,
    square=True, 
    linewidths=1, 
    cbar_kws={'shrink': 0.8, 'label': 'Pearson Correlation'}
)
plt.title('Figure 5: Correlation Matrix Heatmap of Preprocessed Titanic Features', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('figures/figure5_correlation_heatmap.png', dpi=300)
plt.close()

print("All 5 figures generated and saved successfully!")
