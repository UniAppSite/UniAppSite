import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Read the CSV file
df = pd.read_csv('DATA.csv')

# Clean column names (remove extra spaces and special characters)
df.columns = df.columns.str.strip()

# Rename columns for easier access
df.columns = ['Sex', 'Type_Of_Disease', 'Religion']

# Clean the data - strip whitespace and handle common data issues
df['Sex'] = df['Sex'].str.strip()
df['Type_Of_Disease'] = df['Type_Of_Disease'].str.strip()
df['Religion'] = df['Religion'].str.strip()

# Fix known data entry errors
df['Sex'] = df['Sex'].replace({'Make': 'Male', 'Female=': 'Female', 'Male ': 'Male'})

# Replace empty strings with NaN for proper missing data handling
df.replace('', np.nan, inplace=True)

# Calculate total valid responses for each column
total_records = len(df)
valid_sex = df['Sex'].notna().sum()
valid_disease = df['Type_Of_Disease'].notna().sum()
valid_religion = df['Religion'].notna().sum()

print("="*60)
print("DATA ANALYSIS SUMMARY")
print("="*60)
print(f"Total Records: {total_records}")
print(f"Valid Sex entries: {valid_sex} ({valid_sex/total_records*100:.2f}%)")
print(f"Valid Disease Type entries: {valid_disease} ({valid_disease/total_records*100:.2f}%)")
print(f"Valid Religion entries: {valid_religion} ({valid_religion/total_records*100:.2f}%)")
print(f"Missing Sex entries: {total_records - valid_sex}")
print(f"Missing Disease Type entries: {total_records - valid_disease}")
print(f"Missing Religion entries: {total_records - valid_religion}")
print("="*60)

# ============================================================================
# 1. SEX OF AFFECTED INDIVIDUAL (PIE CHART)
# ============================================================================
print("\n1. SEX DISTRIBUTION")
print("-"*60)

# Filter out missing values for sex
sex_data = df['Sex'].dropna()
sex_counts = sex_data.value_counts()

print(f"Total valid responses: {len(sex_data)}")
for sex, count in sex_counts.items():
    percentage = (count / len(sex_data)) * 100
    print(f"{sex}: {count} ({percentage:.2f}%)")

# Create pie chart for Sex
plt.figure(figsize=(10, 8))
colors = ['#3498db', '#e74c3c']
explode = (0.05, 0.05)

wedges, texts, autotexts = plt.pie(
    sex_counts.values, 
    labels=sex_counts.index, 
    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(sex_counts.values))})',
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 12, 'weight': 'bold'}
)

plt.title('Sex Distribution of Affected Individuals', 
          fontsize=16, weight='bold', pad=20)
plt.text(0, -1.3, f'Total Valid Responses: {len(sex_data)}', 
         ha='center', fontsize=11, style='italic')
plt.axis('equal')
plt.tight_layout()
plt.savefig('sex_distribution_piechart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: sex_distribution_piechart.png")

# Create a simple Male:Female ratio pie chart
plt.figure(figsize=(10, 8))
colors = ['#3498db', '#e74c3c']
explode = (0.05, 0.05)

# Calculate ratio
male_count = sex_counts.get('Male', 0)
female_count = sex_counts.get('Female', 0)
total = male_count + female_count

wedges, texts, autotexts = plt.pie(
    [male_count, female_count], 
    labels=['Male', 'Female'], 
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 14, 'weight': 'bold'}
)

# Add count in the center
plt.text(0, 0, f'Male:Female\n{male_count}:{female_count}', 
         ha='center', va='center', fontsize=13, weight='bold',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.title('Sex Ratio of Affected Individuals\n(Male : Female)', 
          fontsize=16, weight='bold', pad=20)
plt.text(0, -1.3, f'Total: {total} individuals', 
         ha='center', fontsize=11, style='italic')
plt.axis('equal')
plt.tight_layout()
plt.savefig('sex_ratio_piechart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: sex_ratio_piechart.png")

# ============================================================================
# 2. TYPE OF DISEASES (PIE CHART)
# ============================================================================
print("\n2. DISEASE TYPE DISTRIBUTION")
print("-"*60)

# Filter out missing values for disease type
disease_data = df['Type_Of_Disease'].dropna()
disease_counts = disease_data.value_counts()

print(f"Total valid responses: {len(disease_data)}")
for disease, count in disease_counts.items():
    percentage = (count / len(disease_data)) * 100
    print(f"{disease}: {count} ({percentage:.2f}%)")

# Create pie chart for Disease Type
plt.figure(figsize=(14, 10))
colors = plt.cm.Set3(range(len(disease_counts)))

# Use autopct for percentages only, move labels to legend
wedges, texts, autotexts = plt.pie(
    disease_counts.values, 
    labels=None,  # Remove labels from pie chart
    autopct=lambda pct: f'{pct:.1f}%' if pct > 3 else '',  # Only show percentage if > 3%
    startangle=90,
    colors=colors,
    textprops={'fontsize': 11, 'weight': 'bold'},
    pctdistance=0.85
)

# Make percentage text bold and black
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_weight('bold')

# Create legend with disease names and counts
legend_labels = [f'{disease}: {count} ({count/len(disease_data)*100:.1f}%)' 
                 for disease, count in disease_counts.items()]
plt.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5), 
          fontsize=10, title='Disease Type', title_fontsize=12)

plt.title('Disease Type Distribution', 
          fontsize=16, weight='bold', pad=20)
plt.text(0, -1.2, f'Total Valid Responses: {len(disease_data)}', 
         ha='center', fontsize=11, style='italic')
plt.axis('equal')
plt.tight_layout()
plt.savefig('disease_type_piechart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: disease_type_piechart.png")

# ============================================================================
# 3. COMPARATIVE ANALYSIS: AGE, TYPE OF DISEASE, RELIGION
# ============================================================================
print("\n3. COMPARATIVE ANALYSIS")
print("-"*60)

# Note: Age data is not present in the CSV, so we'll focus on Disease Type vs Religion
# Create a clean dataset for comparative analysis
df_clean = df[df['Type_Of_Disease'].notna() & df['Religion'].notna()].copy()

print(f"Records with both Disease Type and Religion: {len(df_clean)}")

# ----------------------------------------------------------------------------
# 3a. Disease Type by Religion (Grouped Bar Chart)
# ----------------------------------------------------------------------------
disease_religion_crosstab = pd.crosstab(
    df_clean['Type_Of_Disease'], 
    df_clean['Religion']
)

print("\nDisease Type by Religion Cross-tabulation:")
print(disease_religion_crosstab)

# Create grouped bar chart
fig, ax = plt.subplots(figsize=(16, 10))
disease_religion_crosstab.plot(kind='bar', ax=ax, width=0.8, edgecolor='black')

plt.title('Disease Type Distribution by Religion', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Type of Disease', fontsize=13, weight='bold')
plt.ylabel('Number of Cases', fontsize=13, weight='bold')
plt.legend(title='Religion', title_fontsize=12, fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for container in ax.containers:
    ax.bar_label(container, label_type='edge', padding=3, fontsize=9)

plt.tight_layout()
plt.savefig('disease_by_religion_barchart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: disease_by_religion_barchart.png")

# ----------------------------------------------------------------------------
# 3b. Religion Distribution by Disease Type (Stacked Bar Chart) - FIXED
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(16, 10))

# Calculate percentages correctly - divide by row sum
disease_religion_crosstab_pct = disease_religion_crosstab.div(
    disease_religion_crosstab.sum(axis=1), axis=0
) * 100

# Plot with correct data
disease_religion_crosstab_pct.plot(
    kind='bar', 
    stacked=True, 
    ax=ax, 
    width=0.8,
    edgecolor='black',
    alpha=0.8
)

plt.title('Religion Distribution within Each Disease Type (%)', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Type of Disease', fontsize=13, weight='bold')
plt.ylabel('Percentage (%)', fontsize=13, weight='bold')
plt.legend(title='Religion', title_fontsize=12, fontsize=11, loc='upper right')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.ylim(0, 100)
plt.yticks(range(0, 101, 10))

plt.tight_layout()
plt.savefig('religion_percentage_by_disease_stacked.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: religion_percentage_by_disease_stacked.png")

# ----------------------------------------------------------------------------
# 3c. Sex vs Disease Type (Grouped Bar Chart)
# ----------------------------------------------------------------------------
df_sex_disease = df[df['Type_Of_Disease'].notna() & df['Sex'].notna()].copy()
sex_disease_crosstab = pd.crosstab(
    df_sex_disease['Type_Of_Disease'], 
    df_sex_disease['Sex']
)

print("\nDisease Type by Sex Cross-tabulation:")
print(sex_disease_crosstab)

fig, ax = plt.subplots(figsize=(16, 10))
sex_disease_crosstab.plot(kind='bar', ax=ax, width=0.8, edgecolor='black', color=['#3498db', '#e74c3c'])

plt.title('Disease Type Distribution by Sex', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Type of Disease', fontsize=13, weight='bold')
plt.ylabel('Number of Cases', fontsize=13, weight='bold')
plt.legend(title='Sex', title_fontsize=12, fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for container in ax.containers:
    ax.bar_label(container, label_type='edge', padding=3, fontsize=9)

plt.tight_layout()
plt.savefig('disease_by_sex_barchart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: disease_by_sex_barchart.png")

# ----------------------------------------------------------------------------
# 3d. Religion Distribution (Bar Chart with counts and percentages)
# ----------------------------------------------------------------------------
religion_data = df['Religion'].dropna()
religion_counts = religion_data.value_counts()

print("\nReligion Distribution:")
print(f"Total valid responses: {len(religion_data)}")
for religion, count in religion_counts.items():
    percentage = (count / len(religion_data)) * 100
    print(f"{religion}: {count} ({percentage:.2f}%)")

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.bar(
    religion_counts.index, 
    religion_counts.values,
    color=['#2ecc71', '#3498db', '#9b59b6'],
    edgecolor='black',
    linewidth=1.5
)

plt.title('Religion Distribution of Affected Individuals', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Religion', fontsize=13, weight='bold')
plt.ylabel('Number of Cases', fontsize=13, weight='bold')
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add value and percentage labels on bars
for i, (bar, count) in enumerate(zip(bars, religion_counts.values)):
    height = bar.get_height()
    percentage = (count / len(religion_data)) * 100
    ax.text(
        bar.get_x() + bar.get_width()/2., 
        height,
        f'{count}\n({percentage:.1f}%)',
        ha='center', 
        va='bottom',
        fontsize=11,
        weight='bold'
    )

plt.text(
    0.5, -0.15, 
    f'Total Valid Responses: {len(religion_data)}', 
    ha='center', 
    transform=ax.transAxes,
    fontsize=11, 
    style='italic'
)

plt.tight_layout()
plt.savefig('religion_distribution_barchart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: religion_distribution_barchart.png")

# ----------------------------------------------------------------------------
# 3e. Heatmap of Disease Type vs Religion
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 10))
im = ax.imshow(disease_religion_crosstab.values, cmap='YlOrRd', aspect='auto')

# Set ticks and labels
ax.set_xticks(np.arange(len(disease_religion_crosstab.columns)))
ax.set_yticks(np.arange(len(disease_religion_crosstab.index)))
ax.set_xticklabels(disease_religion_crosstab.columns)
ax.set_yticklabels(disease_religion_crosstab.index)

# Rotate the tick labels for better readability
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Number of Cases', rotation=270, labelpad=20, fontsize=12, weight='bold')

# Add text annotations with black text only
for i in range(len(disease_religion_crosstab.index)):
    for j in range(len(disease_religion_crosstab.columns)):
        value = disease_religion_crosstab.values[i, j]
        text = ax.text(j, i, int(value), ha="center", va="center", 
                      color="black",
                      fontsize=10, weight='bold')

plt.title('Disease Type vs Religion Heatmap', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Religion', fontsize=13, weight='bold')
plt.ylabel('Type of Disease', fontsize=13, weight='bold')
plt.tight_layout()
plt.savefig('disease_religion_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: disease_religion_heatmap.png")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print("\nGenerated Files:")
print("1. sex_distribution_piechart.png")
print("2. sex_ratio_piechart.png (Male:Female ratio)")
print("3. disease_type_piechart.png")
print("4. disease_by_religion_barchart.png")
print("5. religion_percentage_by_disease_stacked.png")
print("6. disease_by_sex_barchart.png")
print("7. religion_distribution_barchart.png")
print("8. disease_religion_heatmap.png")
print("="*60)
