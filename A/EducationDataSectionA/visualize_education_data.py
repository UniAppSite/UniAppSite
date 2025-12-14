import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Read the CSV file
try:
    df = pd.read_csv('DATA.csv')
    print("Data loaded successfully!")
    print(f"Total rows in dataset: {len(df)}")
except FileNotFoundError:
    print("Error: DATA.csv file not found!")
    exit()
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

# Clean column names (remove extra spaces and newlines)
df.columns = df.columns.str.strip().str.replace('\n', ' ')

# Identify the correct column names
education_col = '7) Highest Education Level Completed(of respondent):'
consanguineous_col = '2) Is your marriage consanguineous (i.e., with a blood relative)?'
relation_col = '(If Yes) What is the relation between you and your spouse?'

# Clean the data
df[education_col] = df[education_col].str.strip()
df[consanguineous_col] = df[consanguineous_col].str.strip()
df[relation_col] = df[relation_col].str.strip()

# Remove rows with missing education data
df_clean = df[df[education_col].notna() & (df[education_col] != '')]
print(f"Rows with valid education data: {len(df_clean)}")

# ================================================================================
# 1) PIE CHART FOR HIGHEST EDUCATION LEVEL COMPLETED
# ================================================================================

# Count education levels and calculate percentages
education_counts = df_clean[education_col].value_counts()
total_valid_education = len(df_clean)

# Calculate percentages
education_percentages = (education_counts / total_valid_education * 100).round(2)

# Create figure for pie chart
fig1, ax1 = plt.subplots(figsize=(12, 10))

# Define colors (colorful palette)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']

# Create pie chart with better spacing
wedges, texts, autotexts = ax1.pie(
    education_counts.values,
    labels=None,  # We'll add custom labels
    autopct='',  # We'll add custom text
    startangle=90,
    colors=colors[:len(education_counts)],
    pctdistance=0.85,
    textprops={'color': 'black', 'fontsize': 10, 'weight': 'bold'}
)

# Add custom labels with count and percentage
labels_with_data = []
for i, (edu_level, count) in enumerate(education_counts.items()):
    percentage = education_percentages[edu_level]
    label = f'{edu_level}\nCount: {count}\n({percentage}%)'
    labels_with_data.append(label)

# Add legend outside the pie chart to avoid overlapping
ax1.legend(
    labels_with_data,
    loc='center left',
    bbox_to_anchor=(1, 0, 0.5, 1),
    fontsize=9,
    frameon=True,
    fancybox=False,
    shadow=False
)

# Title and total information
ax1.set_title(
    'Highest Education Level Completed (of Respondent)',
    fontsize=14,
    weight='bold',
    color='black',
    pad=20
)

# Add total valid responses text box
textstr = f'Total Valid Responses: {total_valid_education}'
props = dict(boxstyle='round', facecolor='white', edgecolor='black', linewidth=1.5)
ax1.text(
    0.5, -0.15,
    textstr,
    transform=ax1.transAxes,
    fontsize=11,
    weight='bold',
    color='black',
    verticalalignment='top',
    horizontalalignment='center',
    bbox=props
)

plt.tight_layout()
plt.savefig('education_level_piechart.png', dpi=300, bbox_inches='tight', facecolor='white')
print("\n✓ Pie chart saved as 'education_level_piechart.png'")
plt.close()

# Print summary
print("\n" + "="*70)
print("EDUCATION LEVEL DISTRIBUTION SUMMARY")
print("="*70)
for edu_level, count in education_counts.items():
    percentage = education_percentages[edu_level]
    print(f"{edu_level:30s} | Count: {count:3d} | Percentage: {percentage:6.2f}%")
print("-"*70)
print(f"{'TOTAL VALID RESPONSES':30s} | Count: {total_valid_education:3d} | Percentage: 100.00%")
print("="*70)

# ================================================================================
# 2) COMPARATIVE ANALYSIS: EDUCATION vs CONSANGUINEOUS MARRIAGE vs RELATION
# ================================================================================

# Clean and prepare data for comparison
df_compare = df_clean.copy()

# Handle missing values in consanguineous column
df_compare[consanguineous_col] = df_compare[consanguineous_col].fillna('Unknown')

# Handle missing values in relation column
df_compare[relation_col] = df_compare[relation_col].fillna('None')

# Standardize consanguineous responses
df_compare[consanguineous_col] = df_compare[consanguineous_col].replace({
    'Yes': 'Yes',
    'No': 'No',
    'yes': 'Yes',
    'no': 'No'
})

# Create cross-tabulation
crosstab = pd.crosstab(
    [df_compare[education_col], df_compare[consanguineous_col]],
    df_compare[relation_col],
    margins=False
)

print("\n" + "="*70)
print("CROSS-TABULATION: EDUCATION vs CONSANGUINEOUS vs RELATION")
print("="*70)
print(crosstab)

# ================================================================================
# VISUALIZATION 1: Grouped Bar Chart - Education Level vs Consanguineous Marriage
# ================================================================================

# Create pivot table for education vs consanguineous
pivot_edu_consang = df_compare.groupby([education_col, consanguineous_col]).size().unstack(fill_value=0)

# Calculate percentages for each education level
pivot_edu_consang_pct = pivot_edu_consang.div(pivot_edu_consang.sum(axis=1), axis=0) * 100

# Create figure
fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(16, 8))

# Sort education levels for better visualization
education_order = ['No formal education', 'Primary School', 'Secondary School', 
                   'Secondary school ', 'Graduate', 'Postgraduate', 'Postgraduate ']
education_order = [e for e in education_order if e in pivot_edu_consang.index]
pivot_edu_consang = pivot_edu_consang.reindex(education_order, fill_value=0)
pivot_edu_consang_pct = pivot_edu_consang_pct.reindex(education_order, fill_value=0)

# Plot 1: Count
x = np.arange(len(pivot_edu_consang.index))
width = 0.35

# Get columns that exist
available_cols = pivot_edu_consang.columns.tolist()
bars = []

for i, col in enumerate(available_cols):
    offset = width * (i - len(available_cols)/2 + 0.5)
    bar = ax2.bar(x + offset, pivot_edu_consang[col], width, 
                   label=f'{col}', color=['#FF6B6B', '#4ECDC4', '#45B7D1'][i % 3],
                   edgecolor='black', linewidth=0.5)
    bars.append(bar)
    
    # Add count labels on bars
    for j, (idx, val) in enumerate(pivot_edu_consang[col].items()):
        if val > 0:
            ax2.text(x[j] + offset, val + 0.5, str(int(val)),
                    ha='center', va='bottom', fontsize=8, weight='bold', color='black')

ax2.set_xlabel('Education Level', fontsize=11, weight='bold', color='black')
ax2.set_ylabel('Count', fontsize=11, weight='bold', color='black')
ax2.set_title('Education Level vs Consanguineous Marriage (Count)', 
              fontsize=12, weight='bold', color='black', pad=15)
ax2.set_xticks(x)
ax2.set_xticklabels(pivot_edu_consang.index, rotation=45, ha='right', fontsize=9, color='black')
ax2.legend(title='Consanguineous\nMarriage', loc='upper left', fontsize=9, 
          title_fontsize=10, frameon=True)
ax2.grid(axis='y', alpha=0.3, linestyle='--', color='gray')
ax2.tick_params(colors='black')

# Plot 2: Percentage
bars2 = []
for i, col in enumerate(available_cols):
    offset = width * (i - len(available_cols)/2 + 0.5)
    bar = ax3.bar(x + offset, pivot_edu_consang_pct[col], width,
                   label=f'{col}', color=['#FF6B6B', '#4ECDC4', '#45B7D1'][i % 3],
                   edgecolor='black', linewidth=0.5)
    bars2.append(bar)
    
    # Add percentage labels on bars
    for j, (idx, val) in enumerate(pivot_edu_consang_pct[col].items()):
        if val > 0:
            ax3.text(x[j] + offset, val + 1, f'{val:.1f}%',
                    ha='center', va='bottom', fontsize=8, weight='bold', color='black')

ax3.set_xlabel('Education Level', fontsize=11, weight='bold', color='black')
ax3.set_ylabel('Percentage (%)', fontsize=11, weight='bold', color='black')
ax3.set_title('Education Level vs Consanguineous Marriage (Percentage)', 
              fontsize=12, weight='bold', color='black', pad=15)
ax3.set_xticks(x)
ax3.set_xticklabels(pivot_edu_consang_pct.index, rotation=45, ha='right', fontsize=9, color='black')
ax3.legend(title='Consanguineous\nMarriage', loc='upper left', fontsize=9,
          title_fontsize=10, frameon=True)
ax3.grid(axis='y', alpha=0.3, linestyle='--', color='gray')
ax3.tick_params(colors='black')
ax3.set_ylim(0, 110)

# Add total valid responses
total_text = f'Total Valid Responses: {len(df_compare)}'
fig2.text(0.5, 0.02, total_text, ha='center', fontsize=11, weight='bold', 
         color='black', bbox=dict(boxstyle='round', facecolor='white', 
         edgecolor='black', linewidth=1.5))

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('education_vs_consanguineous.png', dpi=300, bbox_inches='tight', facecolor='white')
print("\n✓ Comparison chart saved as 'education_vs_consanguineous.png'")
plt.close()

# ================================================================================
# VISUALIZATION 2: Stacked Bar Chart - Relation Type by Education Level
# ================================================================================

# Filter only consanguineous marriages (where relationship exists)
df_consang_yes = df_compare[df_compare[consanguineous_col] == 'Yes'].copy()

if len(df_consang_yes) > 0:
    # Create pivot for relation types
    pivot_relation = df_consang_yes.groupby([education_col, relation_col]).size().unstack(fill_value=0)
    pivot_relation = pivot_relation.reindex(education_order, fill_value=0)
    
    # Calculate percentages
    pivot_relation_pct = pivot_relation.div(pivot_relation.sum(axis=1), axis=0) * 100
    
    # Create figure
    fig3, (ax4, ax5) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Define colors for relation types
    relation_colors = {
        'First degree': '#E74C3C',
        'Second degree': '#3498DB',
        'Third degree': '#2ECC71',
        'None': '#F39C12'
    }
    
    # Plot 1: Count - Stacked Bar
    bottom_count = np.zeros(len(pivot_relation))
    
    for col in pivot_relation.columns:
        color = relation_colors.get(col, '#D0D0D0')
        bars = ax4.bar(range(len(pivot_relation)), pivot_relation[col], 
                       label=col, bottom=bottom_count, color=color,
                       edgecolor='black', linewidth=0.5)
        
        # Add count labels
        for i, (idx, val) in enumerate(pivot_relation[col].items()):
            if val > 0:
                y_pos = bottom_count[i] + val/2
                ax4.text(i, y_pos, str(int(val)), ha='center', va='center',
                        fontsize=8, weight='bold', color='black')
        
        bottom_count += pivot_relation[col].values
    
    ax4.set_xlabel('Education Level', fontsize=11, weight='bold', color='black')
    ax4.set_ylabel('Count', fontsize=11, weight='bold', color='black')
    ax4.set_title('Relation Type by Education Level - Consanguineous Marriages (Count)',
                  fontsize=12, weight='bold', color='black', pad=15)
    ax4.set_xticks(range(len(pivot_relation)))
    ax4.set_xticklabels(pivot_relation.index, rotation=45, ha='right', fontsize=9, color='black')
    ax4.legend(title='Relation Type', loc='upper left', fontsize=9,
              title_fontsize=10, frameon=True)
    ax4.grid(axis='y', alpha=0.3, linestyle='--', color='gray')
    ax4.tick_params(colors='black')
    
    # Plot 2: Percentage - Stacked Bar
    bottom_pct = np.zeros(len(pivot_relation_pct))
    
    for col in pivot_relation_pct.columns:
        color = relation_colors.get(col, '#D0D0D0')
        bars = ax5.bar(range(len(pivot_relation_pct)), pivot_relation_pct[col],
                       label=col, bottom=bottom_pct, color=color,
                       edgecolor='black', linewidth=0.5)
        
        # Add percentage labels
        for i, (idx, val) in enumerate(pivot_relation_pct[col].items()):
            if val > 2:  # Only show label if percentage > 2%
                y_pos = bottom_pct[i] + val/2
                ax5.text(i, y_pos, f'{val:.1f}%', ha='center', va='center',
                        fontsize=8, weight='bold', color='black')
        
        bottom_pct += pivot_relation_pct[col].values
    
    ax5.set_xlabel('Education Level', fontsize=11, weight='bold', color='black')
    ax5.set_ylabel('Percentage (%)', fontsize=11, weight='bold', color='black')
    ax5.set_title('Relation Type by Education Level - Consanguineous Marriages (Percentage)',
                  fontsize=12, weight='bold', color='black', pad=15)
    ax5.set_xticks(range(len(pivot_relation_pct)))
    ax5.set_xticklabels(pivot_relation_pct.index, rotation=45, ha='right', fontsize=9, color='black')
    ax5.legend(title='Relation Type', loc='upper left', fontsize=9,
              title_fontsize=10, frameon=True)
    ax5.grid(axis='y', alpha=0.3, linestyle='--', color='gray')
    ax5.tick_params(colors='black')
    ax5.set_ylim(0, 105)
    
    # Add total valid responses
    total_consang = len(df_consang_yes)
    total_text = f'Total Consanguineous Marriages: {total_consang}'
    fig3.text(0.5, 0.02, total_text, ha='center', fontsize=11, weight='bold',
             color='black', bbox=dict(boxstyle='round', facecolor='white',
             edgecolor='black', linewidth=1.5))
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('relation_type_by_education.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Relation type chart saved as 'relation_type_by_education.png'")
    plt.close()

# ================================================================================
# SUMMARY STATISTICS
# ================================================================================

print("\n" + "="*70)
print("EDUCATION vs CONSANGUINEOUS MARRIAGE SUMMARY")
print("="*70)
for edu_level in pivot_edu_consang.index:
    print(f"\n{edu_level}:")
    total_edu = pivot_edu_consang.loc[edu_level].sum()
    for consang in pivot_edu_consang.columns:
        count = pivot_edu_consang.loc[edu_level, consang]
        pct = pivot_edu_consang_pct.loc[edu_level, consang]
        print(f"  {consang:15s} | Count: {int(count):3d} | Percentage: {pct:6.2f}%")
    print(f"  {'TOTAL':15s} | Count: {int(total_edu):3d}")

print("\n" + "="*70)
print("RELATION TYPE DISTRIBUTION (CONSANGUINEOUS MARRIAGES ONLY)")
print("="*70)
if len(df_consang_yes) > 0:
    relation_counts = df_consang_yes[relation_col].value_counts()
    relation_pct = (relation_counts / len(df_consang_yes) * 100).round(2)
    
    for relation, count in relation_counts.items():
        pct = relation_pct[relation]
        print(f"{relation:30s} | Count: {int(count):3d} | Percentage: {pct:6.2f}%")
    print("-"*70)
    print(f"{'TOTAL':30s} | Count: {len(df_consang_yes):3d} | Percentage: 100.00%")
else:
    print("No consanguineous marriages found in the dataset.")

print("="*70)
print("\n✓ All visualizations completed successfully!")
print("\nGenerated files:")
print("  1. education_level_piechart.png")
print("  2. education_vs_consanguineous.png")
print("  3. relation_type_by_education.png")
