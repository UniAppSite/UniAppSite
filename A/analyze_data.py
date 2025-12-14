import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

# Read the CSV file
df = pd.read_csv('DATA.csv')

# Clean column names (remove extra spaces and special characters)
df.columns = df.columns.str.strip()

# Rename columns for easier access
df.columns = ['Sex', 'Type_Of_Disease', 'Religion', 'Consanguinity']

# Clean the data - strip whitespace and handle common data issues
df['Sex'] = df['Sex'].str.strip()
df['Type_Of_Disease'] = df['Type_Of_Disease'].str.strip()
df['Religion'] = df['Religion'].str.strip()
df['Consanguinity'] = df['Consanguinity'].str.strip()

# Fix known data entry errors
df['Sex'] = df['Sex'].replace({'Make': 'Male', 'Female=': 'Female', 'Male ': 'Male'})

# Replace empty strings with NaN for proper missing data handling
df.replace('', np.nan, inplace=True)

# Calculate total valid responses for each column
total_records = len(df)
valid_sex = df['Sex'].notna().sum()
valid_disease = df['Type_Of_Disease'].notna().sum()
valid_religion = df['Religion'].notna().sum()
valid_consanguinity = df['Consanguinity'].notna().sum()

print("="*60)
print("DATA ANALYSIS SUMMARY")
print("="*60)
print(f"Total Records: {total_records}")
print(f"Valid Sex entries: {valid_sex} ({valid_sex/total_records*100:.2f}%)")
print(f"Valid Disease Type entries: {valid_disease} ({valid_disease/total_records*100:.2f}%)")
print(f"Valid Religion entries: {valid_religion} ({valid_religion/total_records*100:.2f}%)")
print(f"Valid Consanguinity entries: {valid_consanguinity} ({valid_consanguinity/total_records*100:.2f}%)")
print(f"Missing Sex entries: {total_records - valid_sex}")
print(f"Missing Disease Type entries: {total_records - valid_disease}")
print(f"Missing Religion entries: {total_records - valid_religion}")
print(f"Missing Consanguinity entries: {total_records - valid_consanguinity}")
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
# 4. CONSANGUINITY ANALYSIS
# ============================================================================
print("\n4. CONSANGUINITY ANALYSIS")
print("-"*60)

# Consanguinity Distribution
consanguinity_data = df['Consanguinity'].dropna()
consanguinity_counts = consanguinity_data.value_counts()

print(f"Total valid responses: {len(consanguinity_data)}")
for status, count in consanguinity_counts.items():
    percentage = (count / len(consanguinity_data)) * 100
    print(f"{status}: {count} ({percentage:.2f}%)")

# ----------------------------------------------------------------------------
# 4a. Consanguinity Distribution (Pie Chart)
# ----------------------------------------------------------------------------
plt.figure(figsize=(10, 8))
colors = ['#e74c3c', '#2ecc71']  # Red for Yes, Green for No
explode = (0.05, 0.05)

wedges, texts, autotexts = plt.pie(
    consanguinity_counts.values, 
    labels=consanguinity_counts.index, 
    autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*sum(consanguinity_counts.values))})',
    startangle=90,
    colors=colors,
    explode=explode,
    textprops={'fontsize': 12, 'weight': 'bold'}
)

plt.title('Consanguineous Marriage Distribution', 
          fontsize=16, weight='bold', pad=20)
plt.text(0, -1.3, f'Total Valid Responses: {len(consanguinity_data)}', 
         ha='center', fontsize=11, style='italic')
plt.axis('equal')
plt.tight_layout()
plt.savefig('consanguinity_piechart.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: consanguinity_piechart.png")

# ----------------------------------------------------------------------------
# 4b. Consanguinity vs Sex (Grouped Bar Chart)
# ----------------------------------------------------------------------------
df_cons_sex = df[df['Consanguinity'].notna() & df['Sex'].notna()].copy()
cons_sex_crosstab = pd.crosstab(df_cons_sex['Consanguinity'], df_cons_sex['Sex'])

print("\nConsanguinity by Sex Cross-tabulation:")
print(cons_sex_crosstab)
print(f"Total valid responses: {len(df_cons_sex)}")

fig, ax = plt.subplots(figsize=(12, 8))
cons_sex_crosstab.plot(kind='bar', ax=ax, width=0.7, edgecolor='black', 
                       color=['#3498db', '#e74c3c'])

plt.title('Consanguinity Distribution by Sex', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Consanguineous Marriage', fontsize=13, weight='bold')
plt.ylabel('Number of Cases', fontsize=13, weight='bold')
plt.legend(title='Sex', title_fontsize=12, fontsize=11)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add value and percentage labels on bars
for container in ax.containers:
    labels = [f'{int(v)}\n({v/len(df_cons_sex)*100:.1f}%)' if v > 0 else '' 
              for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='edge', padding=3, fontsize=10)

plt.text(0.5, -0.15, f'Total Valid Responses: {len(df_cons_sex)}', 
         ha='center', transform=ax.transAxes, fontsize=11, style='italic')
plt.tight_layout()
plt.savefig('consanguinity_by_sex.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: consanguinity_by_sex.png")

# ----------------------------------------------------------------------------
# 4c. Consanguinity vs Disease Type (Grouped Bar Chart)
# ----------------------------------------------------------------------------
df_cons_disease = df[df['Consanguinity'].notna() & df['Type_Of_Disease'].notna()].copy()
cons_disease_crosstab = pd.crosstab(df_cons_disease['Type_Of_Disease'], 
                                    df_cons_disease['Consanguinity'])

print("\nConsanguinity by Disease Type Cross-tabulation:")
print(cons_disease_crosstab)
print(f"Total valid responses: {len(df_cons_disease)}")

fig, ax = plt.subplots(figsize=(16, 10))
cons_disease_crosstab.plot(kind='bar', ax=ax, width=0.8, edgecolor='black',
                          color=['#2ecc71', '#e74c3c'])

plt.title('Consanguinity Distribution by Disease Type', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Type of Disease', fontsize=13, weight='bold')
plt.ylabel('Number of Cases', fontsize=13, weight='bold')
plt.legend(title='Consanguineous', title_fontsize=12, fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for container in ax.containers:
    ax.bar_label(container, label_type='edge', padding=3, fontsize=9)

plt.text(0.5, -0.2, f'Total Valid Responses: {len(df_cons_disease)}', 
         ha='center', transform=ax.transAxes, fontsize=11, style='italic')
plt.tight_layout()
plt.savefig('consanguinity_by_disease.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: consanguinity_by_disease.png")

# ----------------------------------------------------------------------------
# 4d. Consanguinity Percentage by Disease Type (Stacked Bar Chart)
# ----------------------------------------------------------------------------
cons_disease_pct = cons_disease_crosstab.div(cons_disease_crosstab.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(16, 10))
cons_disease_pct.plot(kind='bar', stacked=True, ax=ax, width=0.8, 
                     edgecolor='black', color=['#2ecc71', '#e74c3c'], alpha=0.8)

plt.title('Consanguinity Percentage within Each Disease Type', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Type of Disease', fontsize=13, weight='bold')
plt.ylabel('Percentage (%)', fontsize=13, weight='bold')
plt.legend(title='Consanguineous', title_fontsize=12, fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.ylim(0, 100)
plt.yticks(range(0, 101, 10))

plt.text(0.5, -0.2, f'Total Valid Responses: {len(df_cons_disease)}', 
         ha='center', transform=ax.transAxes, fontsize=11, style='italic')
plt.tight_layout()
plt.savefig('consanguinity_percentage_by_disease.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: consanguinity_percentage_by_disease.png")

# ----------------------------------------------------------------------------
# 4e. Consanguinity vs Religion (Grouped Bar Chart)
# ----------------------------------------------------------------------------
df_cons_religion = df[df['Consanguinity'].notna() & df['Religion'].notna()].copy()
cons_religion_crosstab = pd.crosstab(df_cons_religion['Religion'], 
                                     df_cons_religion['Consanguinity'])

print("\nConsanguinity by Religion Cross-tabulation:")
print(cons_religion_crosstab)
print(f"Total valid responses: {len(df_cons_religion)}")

fig, ax = plt.subplots(figsize=(12, 8))
cons_religion_crosstab.plot(kind='bar', ax=ax, width=0.7, edgecolor='black',
                           color=['#2ecc71', '#e74c3c'])

plt.title('Consanguinity Distribution by Religion', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Religion', fontsize=13, weight='bold')
plt.ylabel('Number of Cases', fontsize=13, weight='bold')
plt.legend(title='Consanguineous', title_fontsize=12, fontsize=11)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Add value and percentage labels on bars
for container in ax.containers:
    labels = [f'{int(v)}\n({v/len(df_cons_religion)*100:.1f}%)' if v > 0 else '' 
              for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='edge', padding=3, fontsize=10)

plt.text(0.5, -0.15, f'Total Valid Responses: {len(df_cons_religion)}', 
         ha='center', transform=ax.transAxes, fontsize=11, style='italic')
plt.tight_layout()
plt.savefig('consanguinity_by_religion.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: consanguinity_by_religion.png")

# ----------------------------------------------------------------------------
# 4f. Heatmap: Disease Type vs Consanguinity
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 12))
im = ax.imshow(cons_disease_crosstab.values, cmap='RdYlGn_r', aspect='auto')

# Set ticks and labels
ax.set_xticks(np.arange(len(cons_disease_crosstab.columns)))
ax.set_yticks(np.arange(len(cons_disease_crosstab.index)))
ax.set_xticklabels(cons_disease_crosstab.columns)
ax.set_yticklabels(cons_disease_crosstab.index)

# Rotate the tick labels for better readability
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")

# Add colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Number of Cases', rotation=270, labelpad=20, fontsize=12, weight='bold')

# Add text annotations with black text only
for i in range(len(cons_disease_crosstab.index)):
    for j in range(len(cons_disease_crosstab.columns)):
        value = cons_disease_crosstab.values[i, j]
        percentage = (value / cons_disease_crosstab.values[i].sum()) * 100 if cons_disease_crosstab.values[i].sum() > 0 else 0
        text = ax.text(j, i, f'{int(value)}\n({percentage:.1f}%)', 
                      ha="center", va="center", color="black",
                      fontsize=9, weight='bold')

plt.title('Disease Type vs Consanguinity Heatmap', 
          fontsize=16, weight='bold', pad=20)
plt.xlabel('Consanguineous Marriage', fontsize=13, weight='bold')
plt.ylabel('Type of Disease', fontsize=13, weight='bold')
plt.text(0.5, -0.08, f'Total Valid Responses: {len(df_cons_disease)}', 
         ha='center', transform=ax.transAxes, fontsize=11, style='italic')
plt.tight_layout()
plt.savefig('disease_consanguinity_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: disease_consanguinity_heatmap.png")

# ----------------------------------------------------------------------------
# 4g. Combined Analysis: Sex, Disease Type, and Consanguinity
# ----------------------------------------------------------------------------
df_complete = df[df['Sex'].notna() & df['Type_Of_Disease'].notna() & 
                 df['Consanguinity'].notna()].copy()

print(f"\nRecords with Sex, Disease Type, and Consanguinity: {len(df_complete)}")

# Create a summary table
summary_table = df_complete.groupby(['Type_Of_Disease', 'Consanguinity', 'Sex']).size().reset_index(name='Count')
summary_table['Percentage'] = (summary_table['Count'] / len(df_complete)) * 100

print("\nDetailed Cross-tabulation (Disease × Consanguinity × Sex):")
print(summary_table.to_string(index=False))

# ----------------------------------------------------------------------------
# 4h. 3D Analysis: Top Diseases by Consanguinity and Sex
# ----------------------------------------------------------------------------
# Focus on top 5 diseases
top_diseases = df_complete['Type_Of_Disease'].value_counts().head(5).index
df_top = df_complete[df_complete['Type_Of_Disease'].isin(top_diseases)].copy()

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# Yes Consanguinity
df_yes = df_top[df_top['Consanguinity'] == 'Yes']
yes_crosstab = pd.crosstab(df_yes['Type_Of_Disease'], df_yes['Sex'])
yes_crosstab.plot(kind='bar', ax=axes[0], width=0.8, edgecolor='black',
                 color=['#3498db', '#e74c3c'])
axes[0].set_title('Top 5 Diseases - Consanguineous Marriage (Yes)', 
                  fontsize=14, weight='bold', pad=15)
axes[0].set_xlabel('Type of Disease', fontsize=12, weight='bold')
axes[0].set_ylabel('Number of Cases', fontsize=12, weight='bold')
axes[0].legend(title='Sex', title_fontsize=11, fontsize=10)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3, linestyle='--')
for container in axes[0].containers:
    axes[0].bar_label(container, label_type='edge', padding=3, fontsize=9)
axes[0].text(0.5, -0.25, f'Total: {len(df_yes)}', ha='center', 
            transform=axes[0].transAxes, fontsize=10, style='italic')

# No Consanguinity
df_no = df_top[df_top['Consanguinity'] == 'No']
no_crosstab = pd.crosstab(df_no['Type_Of_Disease'], df_no['Sex'])
no_crosstab.plot(kind='bar', ax=axes[1], width=0.8, edgecolor='black',
                color=['#3498db', '#e74c3c'])
axes[1].set_title('Top 5 Diseases - Non-Consanguineous Marriage (No)', 
                  fontsize=14, weight='bold', pad=15)
axes[1].set_xlabel('Type of Disease', fontsize=12, weight='bold')
axes[1].set_ylabel('Number of Cases', fontsize=12, weight='bold')
axes[1].legend(title='Sex', title_fontsize=11, fontsize=10)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(axis='y', alpha=0.3, linestyle='--')
for container in axes[1].containers:
    axes[1].bar_label(container, label_type='edge', padding=3, fontsize=9)
axes[1].text(0.5, -0.25, f'Total: {len(df_no)}', ha='center', 
            transform=axes[1].transAxes, fontsize=10, style='italic')

plt.suptitle('Disease Distribution by Sex and Consanguinity Status', 
             fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig('disease_sex_consanguinity_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: disease_sex_consanguinity_comparison.png")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print("\nGenerated Files:")
print("="*60)
print("SEX ANALYSIS:")
print("1. sex_distribution_piechart.png")
print("2. sex_ratio_piechart.png (Male:Female ratio)")
print("\nDISEASE ANALYSIS:")
print("3. disease_type_piechart.png")
print("4. disease_by_sex_barchart.png")
print("\nRELIGION ANALYSIS:")
print("5. religion_distribution_barchart.png")
print("6. disease_by_religion_barchart.png")
print("7. religion_percentage_by_disease_stacked.png")
print("8. disease_religion_heatmap.png")
print("\nCONSANGUINITY ANALYSIS:")
print("9. consanguinity_piechart.png")
print("10. consanguinity_by_sex.png")
print("11. consanguinity_by_disease.png")
print("12. consanguinity_percentage_by_disease.png")
print("13. consanguinity_by_religion.png")
print("14. disease_consanguinity_heatmap.png")
print("15. disease_sex_consanguinity_comparison.png")
print("="*60)
