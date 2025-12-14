import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Read the CSV file
df = pd.read_csv('Data.csv')

# Rename columns for easier handling
df.columns = ['Consanguineous_Marriage', 'Socioeconomic_Class', 'Location_Type', 'Spouse_Relation']

# Remove completely empty rows
df = df.dropna(how='all')

# Clean the data - remove extra whitespace and newlines
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df = df.apply(lambda x: x.str.replace('\n', '') if x.dtype == "object" else x)

# Calculate total valid responses (rows with at least some data)
total_valid_responses = len(df)

print("="*80)
print(f"TOTAL VALID RESPONSES: {total_valid_responses}")
print("="*80)
print("\n")

# Create figure with subplots
fig = plt.figure(figsize=(16, 12))
fig.suptitle(f'Comprehensive Data Analysis\nTotal Valid Responses: {total_valid_responses}', 
             fontsize=16, fontweight='bold', color='black')

# =============================================================================
# 1. CONSANGUINEOUS MARRIAGE ANALYSIS
# =============================================================================
ax1 = plt.subplot(2, 3, 1)
consang_data = df['Consanguineous_Marriage'].dropna()
consang_counts = consang_data.value_counts()
consang_percentages = (consang_counts / len(consang_data) * 100)

# Create bar chart
bars1 = ax1.bar(range(len(consang_counts)), consang_counts.values, 
                color=['#3498db', '#e74c3c'], edgecolor='black', linewidth=1.5)
ax1.set_xticks(range(len(consang_counts)))
ax1.set_xticklabels(consang_counts.index, color='black', fontweight='bold', fontsize=11)
ax1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax1.set_title('Consanguineous Marriage\n(Blood Relative Marriage)', 
              fontweight='bold', color='black', fontsize=12, pad=10)
ax1.tick_params(colors='black', labelsize=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add count and percentage labels
for i, (bar, count, pct) in enumerate(zip(bars1, consang_counts.values, consang_percentages.values)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

print("CONSANGUINEOUS MARRIAGE ANALYSIS:")
print(f"Valid responses: {len(consang_data)}")
for idx, val in consang_counts.items():
    print(f"  {idx}: {val} ({consang_percentages[idx]:.1f}%)")
print("\n")

# =============================================================================
# 2. SOCIOECONOMIC CLASS DISTRIBUTION
# =============================================================================
ax2 = plt.subplot(2, 3, 2)
socio_data = df['Socioeconomic_Class'].dropna()
socio_counts = socio_data.value_counts().sort_index()
socio_percentages = (socio_counts / len(socio_data) * 100)

colors = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71']
bars2 = ax2.bar(range(len(socio_counts)), socio_counts.values, 
                color=colors[:len(socio_counts)], edgecolor='black', linewidth=1.5)
ax2.set_xticks(range(len(socio_counts)))
ax2.set_xticklabels([f'Class {x}' for x in socio_counts.index], 
                     color='black', fontweight='bold', fontsize=10, rotation=0)
ax2.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax2.set_title('Socioeconomic Class Distribution\n(Modified Kuppuswamy Scale)', 
              fontweight='bold', color='black', fontsize=12, pad=10)
ax2.tick_params(colors='black', labelsize=10)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars2, socio_counts.values, socio_percentages.values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=9)

print("SOCIOECONOMIC CLASS DISTRIBUTION:")
print(f"Valid responses: {len(socio_data)}")
for idx, val in socio_counts.items():
    print(f"  Class {idx}: {val} ({socio_percentages[idx]:.1f}%)")
print("\n")

# =============================================================================
# 3. LOCATION TYPE DISTRIBUTION
# =============================================================================
ax3 = plt.subplot(2, 3, 3)
location_data = df['Location_Type'].dropna()
location_data = location_data[location_data != '']  # Remove empty strings
location_counts = location_data.value_counts()
location_percentages = (location_counts / len(location_data) * 100)

# Map location codes to full names
location_map = {'R': 'Rural', 'S': 'Semi-urban', 'U': 'Urban'}
location_labels = [location_map.get(x, x) for x in location_counts.index]

colors_loc = ['#27ae60', '#f39c12', '#9b59b6']
bars3 = ax3.bar(range(len(location_counts)), location_counts.values, 
                color=colors_loc[:len(location_counts)], edgecolor='black', linewidth=1.5)
ax3.set_xticks(range(len(location_counts)))
ax3.set_xticklabels(location_labels, color='black', fontweight='bold', fontsize=11)
ax3.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax3.set_title('Location Type Distribution', 
              fontweight='bold', color='black', fontsize=12, pad=10)
ax3.tick_params(colors='black', labelsize=10)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars3, location_counts.values, location_percentages.values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

print("LOCATION TYPE DISTRIBUTION:")
print(f"Valid responses: {len(location_data)}")
for idx, val in location_counts.items():
    location_name = location_map.get(idx, idx)
    print(f"  {location_name}: {val} ({location_percentages[idx]:.1f}%)")
print("\n")

# =============================================================================
# 4. SPOUSE RELATION DEGREE (For Consanguineous Marriages)
# =============================================================================
ax4 = plt.subplot(2, 3, 4)
# Filter for Yes marriages and valid relations
relation_data = df[df['Consanguineous_Marriage'] == 'Yes']['Spouse_Relation'].dropna()
relation_data = relation_data[(relation_data != 'None') & (relation_data != '')]
relation_counts = relation_data.value_counts()
relation_percentages = (relation_counts / len(relation_data) * 100)

colors_rel = ['#e74c3c', '#3498db', '#2ecc71']
bars4 = ax4.bar(range(len(relation_counts)), relation_counts.values, 
                color=colors_rel[:len(relation_counts)], edgecolor='black', linewidth=1.5)
ax4.set_xticks(range(len(relation_counts)))
ax4.set_xticklabels(relation_counts.index, color='black', fontweight='bold', fontsize=10, rotation=0)
ax4.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax4.set_title('Spouse Relation Degree\n(For Consanguineous Marriages)', 
              fontweight='bold', color='black', fontsize=12, pad=10)
ax4.tick_params(colors='black', labelsize=10)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars4, relation_counts.values, relation_percentages.values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

print("SPOUSE RELATION DEGREE (Consanguineous Marriages Only):")
print(f"Valid responses: {len(relation_data)}")
for idx, val in relation_counts.items():
    print(f"  {idx}: {val} ({relation_percentages[idx]:.1f}%)")
print("\n")

# =============================================================================
# 5. MISSING DATA ANALYSIS
# =============================================================================
ax5 = plt.subplot(2, 3, 5)
missing_counts = df.isnull().sum()
missing_counts = missing_counts[missing_counts > 0]
missing_percentages = (missing_counts / total_valid_responses * 100)

if len(missing_counts) > 0:
    bars5 = ax5.barh(range(len(missing_counts)), missing_counts.values, 
                     color='#e74c3c', edgecolor='black', linewidth=1.5)
    ax5.set_yticks(range(len(missing_counts)))
    col_labels = [col.replace('_', ' ') for col in missing_counts.index]
    ax5.set_yticklabels(col_labels, color='black', fontweight='bold', fontsize=10)
    ax5.set_xlabel('Missing Count', fontweight='bold', color='black', fontsize=11)
    ax5.set_title('Missing Data Analysis\n(Blank/Empty Values)', 
                  fontweight='bold', color='black', fontsize=12, pad=10)
    ax5.tick_params(colors='black', labelsize=10)
    ax5.spines['top'].set_visible(False)
    ax5.spines['right'].set_visible(False)
    ax5.grid(axis='x', alpha=0.3, linestyle='--')
    
    for bar, count, pct in zip(bars5, missing_counts.values, missing_percentages.values):
        width = bar.get_width()
        ax5.text(width, bar.get_y() + bar.get_height()/2.,
                 f' {int(count)} ({pct:.1f}%)',
                 ha='left', va='center', fontweight='bold', color='black', fontsize=10)
    
    print("MISSING DATA ANALYSIS:")
    for col, count in missing_counts.items():
        print(f"  {col}: {count} missing ({missing_percentages[col]:.1f}%)")
else:
    ax5.text(0.5, 0.5, 'No Missing Data Found', 
             ha='center', va='center', fontsize=14, fontweight='bold', color='black')
    ax5.set_xlim(0, 1)
    ax5.set_ylim(0, 1)
    ax5.axis('off')
    print("MISSING DATA ANALYSIS: No missing data found")

print("\n")

# =============================================================================
# 6. DATA COMPLETENESS PIE CHART
# =============================================================================
ax6 = plt.subplot(2, 3, 6)
total_cells = total_valid_responses * len(df.columns)
filled_cells = total_cells - df.isnull().sum().sum()
missing_cells = total_cells - filled_cells

sizes = [filled_cells, missing_cells]
labels = ['Complete Data', 'Missing Data']
colors_pie = ['#2ecc71', '#e74c3c']
explode = (0.05, 0)

wedges, texts, autotexts = ax6.pie(sizes, labels=labels, colors=colors_pie, 
                                     autopct='%1.1f%%', startangle=90, 
                                     explode=explode, shadow=True,
                                     textprops={'fontweight': 'bold', 'color': 'black', 'fontsize': 11})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)

ax6.set_title('Overall Data Completeness', 
              fontweight='bold', color='black', fontsize=12, pad=10)

# Add count information
completion_rate = (filled_cells / total_cells * 100)
ax6.text(0, -1.3, f'Complete: {filled_cells}/{total_cells} cells ({completion_rate:.1f}%)', 
         ha='center', fontweight='bold', color='black', fontsize=10)

print("DATA COMPLETENESS:")
print(f"  Total cells: {total_cells}")
print(f"  Filled cells: {filled_cells} ({completion_rate:.1f}%)")
print(f"  Missing cells: {missing_cells} ({(missing_cells/total_cells*100):.1f}%)")
print("\n")

# Adjust layout and save
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig('data_analysis_report.png', dpi=300, bbox_inches='tight', facecolor='white')
print("="*80)
print("Analysis complete! Graph saved as 'data_analysis_report.png'")
print("="*80)
plt.show()

# =============================================================================
# COMPARATIVE ANALYSIS SECTION
# =============================================================================
print("\n" + "="*80)
print("DETAILED COMPARATIVE ANALYSIS")
print("="*80 + "\n")

# Create a new figure for comparative analysis
fig2 = plt.figure(figsize=(18, 12))
fig2.suptitle(f'Detailed Comparative Analysis\nTotal Valid Responses: {total_valid_responses}', 
              fontsize=16, fontweight='bold', color='black')

# =============================================================================
# 1. CONSANGUINEOUS MARRIAGE BY LOCATION TYPE
# =============================================================================
ax_c1 = plt.subplot(2, 3, 1)
# Create crosstab
df_clean = df.dropna(subset=['Consanguineous_Marriage', 'Location_Type'])
df_clean = df_clean[df_clean['Location_Type'] != '']
crosstab_loc = pd.crosstab(df_clean['Location_Type'], df_clean['Consanguineous_Marriage'])

# Reorder and rename
location_order = ['R', 'S', 'U']
crosstab_loc = crosstab_loc.reindex([x for x in location_order if x in crosstab_loc.index])
location_labels_full = [location_map.get(x, x) for x in crosstab_loc.index]

x_pos = np.arange(len(crosstab_loc.index))
width = 0.35

if 'Yes' in crosstab_loc.columns and 'No' in crosstab_loc.columns:
    bars_yes = ax_c1.bar(x_pos - width/2, crosstab_loc['Yes'], width, 
                         label='Yes', color='#e74c3c', edgecolor='black', linewidth=1.5)
    bars_no = ax_c1.bar(x_pos + width/2, crosstab_loc['No'], width, 
                        label='No', color='#3498db', edgecolor='black', linewidth=1.5)
    
    # Add count labels
    for bars in [bars_yes, bars_no]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_c1.text(bar.get_x() + bar.get_width()/2., height,
                          f'{int(height)}',
                          ha='center', va='bottom', fontweight='bold', color='black', fontsize=9)

ax_c1.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=11)
ax_c1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax_c1.set_title('Consanguineous Marriage by Location', 
                fontweight='bold', color='black', fontsize=12, pad=10)
ax_c1.set_xticks(x_pos)
ax_c1.set_xticklabels(location_labels_full, color='black', fontweight='bold', fontsize=10)
ax_c1.legend(frameon=True, loc='upper right', fontsize=10)
ax_c1.tick_params(colors='black', labelsize=10)
ax_c1.grid(axis='y', alpha=0.3, linestyle='--')
ax_c1.spines['top'].set_visible(False)
ax_c1.spines['right'].set_visible(False)

print("CONSANGUINEOUS MARRIAGE BY LOCATION TYPE:")
print(crosstab_loc)
for loc_code in crosstab_loc.index:
    loc_name = location_map.get(loc_code, loc_code)
    total_loc = crosstab_loc.loc[loc_code].sum()
    print(f"\n{loc_name}:")
    for marriage_type in crosstab_loc.columns:
        count = crosstab_loc.loc[loc_code, marriage_type]
        pct = (count / total_loc * 100) if total_loc > 0 else 0
        print(f"  {marriage_type}: {count} ({pct:.1f}%)")
print("\n")

# =============================================================================
# 2. CONSANGUINEOUS MARRIAGE BY SOCIOECONOMIC CLASS
# =============================================================================
ax_c2 = plt.subplot(2, 3, 2)
df_clean2 = df.dropna(subset=['Consanguineous_Marriage', 'Socioeconomic_Class'])
crosstab_socio = pd.crosstab(df_clean2['Socioeconomic_Class'], df_clean2['Consanguineous_Marriage'])
crosstab_socio = crosstab_socio.sort_index()

x_pos2 = np.arange(len(crosstab_socio.index))
width2 = 0.35

if 'Yes' in crosstab_socio.columns and 'No' in crosstab_socio.columns:
    bars_yes2 = ax_c2.bar(x_pos2 - width2/2, crosstab_socio['Yes'], width2, 
                          label='Yes', color='#e74c3c', edgecolor='black', linewidth=1.5)
    bars_no2 = ax_c2.bar(x_pos2 + width2/2, crosstab_socio['No'], width2, 
                         label='No', color='#3498db', edgecolor='black', linewidth=1.5)
    
    for bars in [bars_yes2, bars_no2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_c2.text(bar.get_x() + bar.get_width()/2., height,
                          f'{int(height)}',
                          ha='center', va='bottom', fontweight='bold', color='black', fontsize=9)

ax_c2.set_xlabel('Socioeconomic Class', fontweight='bold', color='black', fontsize=11)
ax_c2.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax_c2.set_title('Consanguineous Marriage by Socioeconomic Class', 
                fontweight='bold', color='black', fontsize=12, pad=10)
ax_c2.set_xticks(x_pos2)
ax_c2.set_xticklabels([f'Class {x}' for x in crosstab_socio.index], 
                       color='black', fontweight='bold', fontsize=10)
ax_c2.legend(frameon=True, loc='upper right', fontsize=10)
ax_c2.tick_params(colors='black', labelsize=10)
ax_c2.grid(axis='y', alpha=0.3, linestyle='--')
ax_c2.spines['top'].set_visible(False)
ax_c2.spines['right'].set_visible(False)

print("CONSANGUINEOUS MARRIAGE BY SOCIOECONOMIC CLASS:")
print(crosstab_socio)
for socio_class in crosstab_socio.index:
    total_class = crosstab_socio.loc[socio_class].sum()
    print(f"\nClass {socio_class}:")
    for marriage_type in crosstab_socio.columns:
        count = crosstab_socio.loc[socio_class, marriage_type]
        pct = (count / total_class * 100) if total_class > 0 else 0
        print(f"  {marriage_type}: {count} ({pct:.1f}%)")
print("\n")

# =============================================================================
# 3. SOCIOECONOMIC CLASS BY LOCATION TYPE (STACKED)
# =============================================================================
ax_c3 = plt.subplot(2, 3, 3)
df_clean3 = df.dropna(subset=['Location_Type', 'Socioeconomic_Class'])
df_clean3 = df_clean3[df_clean3['Location_Type'] != '']
crosstab_loc_socio = pd.crosstab(df_clean3['Location_Type'], df_clean3['Socioeconomic_Class'])

location_order2 = ['R', 'S', 'U']
crosstab_loc_socio = crosstab_loc_socio.reindex([x for x in location_order2 if x in crosstab_loc_socio.index])
location_labels_full2 = [location_map.get(x, x) for x in crosstab_loc_socio.index]

colors_stack = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71']
bottom_vals = np.zeros(len(crosstab_loc_socio.index))

for i, col in enumerate(sorted(crosstab_loc_socio.columns)):
    values = crosstab_loc_socio[col].values
    bars = ax_c3.bar(range(len(crosstab_loc_socio.index)), values, 
                     bottom=bottom_vals, label=f'Class {col}',
                     color=colors_stack[i % len(colors_stack)], 
                     edgecolor='black', linewidth=1.2)
    
    # Add count labels
    for j, (bar, val) in enumerate(zip(bars, values)):
        if val > 0:
            ax_c3.text(bar.get_x() + bar.get_width()/2., 
                      bottom_vals[j] + val/2.,
                      f'{int(val)}',
                      ha='center', va='center', fontweight='bold', 
                      color='white', fontsize=9,
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.5))
    
    bottom_vals += values

ax_c3.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax_c3.set_title('Socioeconomic Class Distribution by Location', 
                fontweight='bold', color='black', fontsize=12, pad=10)
ax_c3.set_xticks(range(len(crosstab_loc_socio.index)))
ax_c3.set_xticklabels(location_labels_full2, color='black', fontweight='bold', fontsize=10)
ax_c3.legend(frameon=True, loc='upper right', fontsize=9, ncol=1)
ax_c3.tick_params(colors='black', labelsize=10)
ax_c3.grid(axis='y', alpha=0.3, linestyle='--')
ax_c3.spines['top'].set_visible(False)
ax_c3.spines['right'].set_visible(False)

print("SOCIOECONOMIC CLASS BY LOCATION TYPE:")
print(crosstab_loc_socio)
for loc_code in crosstab_loc_socio.index:
    loc_name = location_map.get(loc_code, loc_code)
    total_loc = crosstab_loc_socio.loc[loc_code].sum()
    print(f"\n{loc_name} (Total: {int(total_loc)}):")
    for socio_class in sorted(crosstab_loc_socio.columns):
        count = crosstab_loc_socio.loc[loc_code, socio_class]
        pct = (count / total_loc * 100) if total_loc > 0 else 0
        print(f"  Class {socio_class}: {count} ({pct:.1f}%)")
print("\n")

# =============================================================================
# 4. PERCENTAGE COMPARISON: CONSANGUINEOUS MARRIAGE RATES
# =============================================================================
ax_c4 = plt.subplot(2, 3, 4)

# Calculate percentages by location
consang_pct_by_loc = []
loc_labels_pct = []
for loc_code in ['R', 'S', 'U']:
    if loc_code in crosstab_loc.index and 'Yes' in crosstab_loc.columns:
        total = crosstab_loc.loc[loc_code].sum()
        yes_count = crosstab_loc.loc[loc_code, 'Yes']
        pct = (yes_count / total * 100) if total > 0 else 0
        consang_pct_by_loc.append(pct)
        loc_labels_pct.append(location_map.get(loc_code, loc_code))

bars_pct = ax_c4.bar(range(len(consang_pct_by_loc)), consang_pct_by_loc,
                     color=['#27ae60', '#f39c12', '#9b59b6'], 
                     edgecolor='black', linewidth=1.5)
ax_c4.set_xticks(range(len(loc_labels_pct)))
ax_c4.set_xticklabels(loc_labels_pct, color='black', fontweight='bold', fontsize=11)
ax_c4.set_ylabel('Percentage (%)', fontweight='bold', color='black', fontsize=11)
ax_c4.set_title('Consanguineous Marriage Rate\nby Location Type', 
                fontweight='bold', color='black', fontsize=12, pad=10)
ax_c4.tick_params(colors='black', labelsize=10)
ax_c4.grid(axis='y', alpha=0.3, linestyle='--')
ax_c4.spines['top'].set_visible(False)
ax_c4.spines['right'].set_visible(False)
ax_c4.set_ylim(0, 100)

for bar, pct in zip(bars_pct, consang_pct_by_loc):
    height = bar.get_height()
    ax_c4.text(bar.get_x() + bar.get_width()/2., height,
              f'{pct:.1f}%',
              ha='center', va='bottom', fontweight='bold', color='black', fontsize=11)

print("CONSANGUINEOUS MARRIAGE RATE BY LOCATION:")
for loc, pct in zip(loc_labels_pct, consang_pct_by_loc):
    print(f"  {loc}: {pct:.1f}%")
print("\n")

# =============================================================================
# 5. RELATION DEGREE DISTRIBUTION BY LOCATION
# =============================================================================
ax_c5 = plt.subplot(2, 3, 5)
df_relation = df[(df['Consanguineous_Marriage'] == 'Yes') & 
                 (df['Spouse_Relation'].notna()) & 
                 (df['Spouse_Relation'] != 'None') &
                 (df['Spouse_Relation'] != '')]
df_relation = df_relation[df_relation['Location_Type'].notna() & (df_relation['Location_Type'] != '')]

if len(df_relation) > 0:
    crosstab_relation = pd.crosstab(df_relation['Spouse_Relation'], df_relation['Location_Type'])
    
    location_order3 = ['R', 'S', 'U']
    crosstab_relation = crosstab_relation[[x for x in location_order3 if x in crosstab_relation.columns]]
    
    x_pos3 = np.arange(len(crosstab_relation.index))
    width3 = 0.25
    
    colors_rel2 = ['#27ae60', '#f39c12', '#9b59b6']
    
    for i, (loc_code, color) in enumerate(zip(crosstab_relation.columns, colors_rel2)):
        offset = (i - 1) * width3
        loc_name = location_map.get(loc_code, loc_code)
        bars = ax_c5.bar(x_pos3 + offset, crosstab_relation[loc_code], width3, 
                        label=loc_name, color=color, edgecolor='black', linewidth=1.2)
        
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_c5.text(bar.get_x() + bar.get_width()/2., height,
                          f'{int(height)}',
                          ha='center', va='bottom', fontweight='bold', color='black', fontsize=8)
    
    ax_c5.set_xlabel('Relation Degree', fontweight='bold', color='black', fontsize=11)
    ax_c5.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
    ax_c5.set_title('Relation Degree by Location\n(Consanguineous Marriages)', 
                    fontweight='bold', color='black', fontsize=12, pad=10)
    ax_c5.set_xticks(x_pos3)
    ax_c5.set_xticklabels(crosstab_relation.index, color='black', fontweight='bold', fontsize=10)
    ax_c5.legend(frameon=True, loc='upper right', fontsize=9)
    ax_c5.tick_params(colors='black', labelsize=10)
    ax_c5.grid(axis='y', alpha=0.3, linestyle='--')
    ax_c5.spines['top'].set_visible(False)
    ax_c5.spines['right'].set_visible(False)
    
    print("RELATION DEGREE BY LOCATION (Consanguineous Marriages):")
    print(crosstab_relation)
    print("\n")
else:
    ax_c5.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center', 
               fontsize=12, fontweight='bold', color='black')
    ax_c5.set_xlim(0, 1)
    ax_c5.set_ylim(0, 1)

# =============================================================================
# 6. HEATMAP: CONSANGUINEOUS MARRIAGE BY CLASS & LOCATION
# =============================================================================
ax_c6 = plt.subplot(2, 3, 6)
df_heatmap = df.dropna(subset=['Consanguineous_Marriage', 'Socioeconomic_Class', 'Location_Type'])
df_heatmap = df_heatmap[df_heatmap['Location_Type'] != '']
df_heatmap_yes = df_heatmap[df_heatmap['Consanguineous_Marriage'] == 'Yes']

if len(df_heatmap_yes) > 0:
    heatmap_data = pd.crosstab(df_heatmap_yes['Socioeconomic_Class'], df_heatmap_yes['Location_Type'])
    
    location_order4 = ['R', 'S', 'U']
    heatmap_data = heatmap_data.reindex(columns=[x for x in location_order4 if x in heatmap_data.columns], fill_value=0)
    heatmap_data = heatmap_data.sort_index()
    
    im = ax_c6.imshow(heatmap_data.values, cmap='YlOrRd', aspect='auto', 
                      interpolation='nearest', vmin=0)
    
    ax_c6.set_xticks(range(len(heatmap_data.columns)))
    ax_c6.set_yticks(range(len(heatmap_data.index)))
    ax_c6.set_xticklabels([location_map.get(x, x) for x in heatmap_data.columns], 
                          color='black', fontweight='bold', fontsize=11)
    ax_c6.set_yticklabels([f'Class {x}' for x in heatmap_data.index], 
                          color='black', fontweight='bold', fontsize=10)
    ax_c6.set_title('Consanguineous Marriage Heatmap\n(Class vs Location)', 
                    fontweight='bold', color='black', fontsize=12, pad=10)
    ax_c6.tick_params(colors='black', labelsize=10)
    
    # Add count annotations
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            count = heatmap_data.iloc[i, j]
            ax_c6.text(j, i, int(count),
                      ha='center', va='center', color='black', 
                      fontweight='bold', fontsize=12)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax_c6, fraction=0.046, pad=0.04)
    cbar.set_label('Count', rotation=270, labelpad=15, fontweight='bold', color='black')
    cbar.ax.tick_params(colors='black')
    
    print("CONSANGUINEOUS MARRIAGE HEATMAP (Class vs Location):")
    print(heatmap_data)
    print("\n")
else:
    ax_c6.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center', 
               fontsize=12, fontweight='bold', color='black')
    ax_c6.set_xlim(0, 1)
    ax_c6.set_ylim(0, 1)

# Adjust layout and save
plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.savefig('comparative_analysis_report.png', dpi=300, bbox_inches='tight', facecolor='white')
print("="*80)
print("Comparative analysis complete! Graph saved as 'comparative_analysis_report.png'")
print("="*80)
plt.show()

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)
print(f"\nTotal Valid Responses: {total_valid_responses}")
print(f"Data Completeness: {completion_rate:.1f}%")

# Overall consanguineous marriage rate
overall_consang_rate = (df['Consanguineous_Marriage'] == 'Yes').sum() / df['Consanguineous_Marriage'].notna().sum() * 100
print(f"\nOverall Consanguineous Marriage Rate: {overall_consang_rate:.1f}%")

# Most common values
print("\nMost Common Values:")
print(f"  Most common location: {df['Location_Type'].mode().values[0] if len(df['Location_Type'].mode()) > 0 else 'N/A'}")
print(f"  Most common socioeconomic class: {df['Socioeconomic_Class'].mode().values[0] if len(df['Socioeconomic_Class'].mode()) > 0 else 'N/A'}")
print(f"  Most common relation degree: {relation_data.mode().values[0] if len(relation_data.mode()) > 0 and len(relation_data) > 0 else 'N/A'}")

print("\n" + "="*80)
print("All analyses complete!")
print("="*80)
