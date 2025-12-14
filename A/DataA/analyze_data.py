import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
plt.style.use('default')
sns.set_palette("husl")

# Read the CSV file
df = pd.read_csv('Data2.csv')

# Clean column names
df.columns = ['socioeconomic_class', 'marriage_consanguineous', 'religion']

# Strip whitespace from string columns
df['marriage_consanguineous'] = df['marriage_consanguineous'].str.strip()
df['religion'] = df['religion'].str.strip()

# Remove rows where all values are missing
df_clean = df.dropna(how='all')

# Convert socioeconomic class to numeric, coercing errors
df_clean['socioeconomic_class'] = pd.to_numeric(df_clean['socioeconomic_class'], errors='coerce')

# Remove rows with missing values for analysis
df_valid = df_clean.dropna()

print(f"Total records: {len(df)}")
print(f"Valid records after cleaning: {len(df_valid)}")
print(f"Missing/Invalid records: {len(df) - len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 1: Socioeconomic Class Distribution
# ===================================================================
print("ANALYSIS 1: Socioeconomic Class Distribution")
print("-" * 60)

socio_counts = df_valid['socioeconomic_class'].value_counts().sort_index()
socio_percentages = (socio_counts / len(df_valid) * 100).round(2)

fig, ax = plt.subplots(figsize=(12, 8))

bars = ax.bar(socio_counts.index, socio_counts.values, 
              color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
              edgecolor='black', linewidth=1.5, alpha=0.8)

# Add count labels on bars
for i, (idx, val) in enumerate(socio_counts.items()):
    height = val
    ax.text(idx, height + 1, f'{int(val)}', 
            ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')
    ax.text(idx, height/2, f'{socio_percentages[idx]:.1f}%', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='black')

ax.set_xlabel('Socioeconomic Class (Kuppuswamy Scale)', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
ax.set_title('Distribution of Socioeconomic Classes', fontsize=16, fontweight='bold', 
             color='black', pad=20)
ax.set_xticks(socio_counts.index)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add total valid responses
ax.text(0.02, 0.98, f'Total Valid Responses: {len(df_valid)}', 
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        color='black')

plt.tight_layout()
plt.savefig('1_socioeconomic_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 1_socioeconomic_distribution.png")

for idx in socio_counts.index:
    print(f"Class {int(idx)}: {socio_counts[idx]} ({socio_percentages[idx]:.2f}%)")
print(f"Total Valid: {len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 2: Marriage Consanguinity Distribution
# ===================================================================
print("ANALYSIS 2: Marriage Consanguinity Distribution")
print("-" * 60)

marriage_counts = df_valid['marriage_consanguineous'].value_counts()
marriage_percentages = (marriage_counts / len(df_valid) * 100).round(2)

fig, ax = plt.subplots(figsize=(10, 8))

colors = ['#FF6B6B', '#4ECDC4']
bars = ax.bar(range(len(marriage_counts)), marriage_counts.values, 
              color=colors[:len(marriage_counts)], edgecolor='black', 
              linewidth=1.5, alpha=0.8)

# Add count and percentage labels
for i, (idx, val) in enumerate(marriage_counts.items()):
    height = val
    ax.text(i, height + 2, f'{int(val)}', 
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='black')
    ax.text(i, height/2, f'{marriage_percentages[idx]:.1f}%', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='black')

ax.set_xlabel('Marriage Type', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
ax.set_title('Distribution of Marriage Consanguinity', fontsize=16, fontweight='bold', 
             color='black', pad=20)
ax.set_xticks(range(len(marriage_counts)))
ax.set_xticklabels(marriage_counts.index, fontsize=12, color='black')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add total valid responses
ax.text(0.02, 0.98, f'Total Valid Responses: {len(df_valid)}', 
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        color='black')

plt.tight_layout()
plt.savefig('2_marriage_consanguinity_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 2_marriage_consanguinity_distribution.png")

for idx in marriage_counts.index:
    print(f"{idx}: {marriage_counts[idx]} ({marriage_percentages[idx]:.2f}%)")
print(f"Total Valid: {len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 3: Religion Distribution
# ===================================================================
print("ANALYSIS 3: Religion Distribution")
print("-" * 60)

religion_counts = df_valid['religion'].value_counts()
religion_percentages = (religion_counts / len(df_valid) * 100).round(2)

fig, ax = plt.subplots(figsize=(10, 8))

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
bars = ax.bar(range(len(religion_counts)), religion_counts.values, 
              color=colors[:len(religion_counts)], edgecolor='black', 
              linewidth=1.5, alpha=0.8)

# Add count and percentage labels
for i, (idx, val) in enumerate(religion_counts.items()):
    height = val
    ax.text(i, height + 2, f'{int(val)}', 
            ha='center', va='bottom', fontsize=13, fontweight='bold', color='black')
    ax.text(i, height/2, f'{religion_percentages[idx]:.1f}%', 
            ha='center', va='center', fontsize=12, fontweight='bold', color='black')

ax.set_xlabel('Religion', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
ax.set_title('Distribution of Religion', fontsize=16, fontweight='bold', 
             color='black', pad=20)
ax.set_xticks(range(len(religion_counts)))
ax.set_xticklabels(religion_counts.index, fontsize=12, color='black')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add total valid responses
ax.text(0.02, 0.98, f'Total Valid Responses: {len(df_valid)}', 
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        color='black')

plt.tight_layout()
plt.savefig('3_religion_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 3_religion_distribution.png")

for idx in religion_counts.index:
    print(f"{idx}: {religion_counts[idx]} ({religion_percentages[idx]:.2f}%)")
print(f"Total Valid: {len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 4: Socioeconomic Class vs Marriage Consanguinity
# ===================================================================
print("ANALYSIS 4: Socioeconomic Class vs Marriage Consanguinity")
print("-" * 60)

crosstab_socio_marriage = pd.crosstab(df_valid['socioeconomic_class'], 
                                       df_valid['marriage_consanguineous'])

fig, ax = plt.subplots(figsize=(12, 8))

x = np.arange(len(crosstab_socio_marriage.index))
width = 0.35

colors = ['#FF6B6B', '#4ECDC4']
for i, col in enumerate(crosstab_socio_marriage.columns):
    bars = ax.bar(x + i*width, crosstab_socio_marriage[col], width, 
                  label=col, color=colors[i], edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add count labels
    for j, (idx, val) in enumerate(crosstab_socio_marriage[col].items()):
        if val > 0:
            percentage = (val / crosstab_socio_marriage.loc[idx].sum() * 100)
            ax.text(j + i*width, val + 0.5, f'{int(val)}\n({percentage:.1f}%)', 
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='black')

ax.set_xlabel('Socioeconomic Class', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
ax.set_title('Socioeconomic Class vs Marriage Consanguinity', fontsize=16, 
             fontweight='bold', color='black', pad=20)
ax.set_xticks(x + width / 2)
ax.set_xticklabels([f'Class {int(i)}' for i in crosstab_socio_marriage.index], 
                    fontsize=11, color='black')
ax.legend(title='Marriage Type', fontsize=11, title_fontsize=12, frameon=True, 
          edgecolor='black')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add total valid responses
ax.text(0.02, 0.98, f'Total Valid Responses: {len(df_valid)}', 
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        color='black')

plt.tight_layout()
plt.savefig('4_socioeconomic_vs_marriage.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 4_socioeconomic_vs_marriage.png")

print(crosstab_socio_marriage)
print(f"\nTotal Valid: {len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 5: Socioeconomic Class vs Religion
# ===================================================================
print("ANALYSIS 5: Socioeconomic Class vs Religion")
print("-" * 60)

crosstab_socio_religion = pd.crosstab(df_valid['socioeconomic_class'], 
                                       df_valid['religion'])

fig, ax = plt.subplots(figsize=(14, 8))

x = np.arange(len(crosstab_socio_religion.index))
width = 0.25

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
for i, col in enumerate(crosstab_socio_religion.columns):
    bars = ax.bar(x + i*width, crosstab_socio_religion[col], width, 
                  label=col, color=colors[i % len(colors)], edgecolor='black', 
                  linewidth=1.5, alpha=0.8)
    
    # Add count labels
    for j, (idx, val) in enumerate(crosstab_socio_religion[col].items()):
        if val > 0:
            percentage = (val / crosstab_socio_religion.loc[idx].sum() * 100)
            ax.text(j + i*width, val + 0.5, f'{int(val)}\n({percentage:.1f}%)', 
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color='black')

ax.set_xlabel('Socioeconomic Class', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
ax.set_title('Socioeconomic Class vs Religion', fontsize=16, 
             fontweight='bold', color='black', pad=20)
ax.set_xticks(x + width * (len(crosstab_socio_religion.columns) - 1) / 2)
ax.set_xticklabels([f'Class {int(i)}' for i in crosstab_socio_religion.index], 
                    fontsize=11, color='black')
ax.legend(title='Religion', fontsize=11, title_fontsize=12, frameon=True, 
          edgecolor='black', loc='upper left')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add total valid responses
ax.text(0.02, 0.98, f'Total Valid Responses: {len(df_valid)}', 
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        color='black')

plt.tight_layout()
plt.savefig('5_socioeconomic_vs_religion.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 5_socioeconomic_vs_religion.png")

print(crosstab_socio_religion)
print(f"\nTotal Valid: {len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 6: Religion vs Marriage Consanguinity
# ===================================================================
print("ANALYSIS 6: Religion vs Marriage Consanguinity")
print("-" * 60)

crosstab_religion_marriage = pd.crosstab(df_valid['religion'], 
                                          df_valid['marriage_consanguineous'])

fig, ax = plt.subplots(figsize=(12, 8))

x = np.arange(len(crosstab_religion_marriage.index))
width = 0.35

colors = ['#FF6B6B', '#4ECDC4']
for i, col in enumerate(crosstab_religion_marriage.columns):
    bars = ax.bar(x + i*width, crosstab_religion_marriage[col], width, 
                  label=col, color=colors[i], edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Add count labels
    for j, (idx, val) in enumerate(crosstab_religion_marriage[col].items()):
        if val > 0:
            percentage = (val / crosstab_religion_marriage.loc[idx].sum() * 100)
            ax.text(j + i*width, val + 0.5, f'{int(val)}\n({percentage:.1f}%)', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

ax.set_xlabel('Religion', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
ax.set_title('Religion vs Marriage Consanguinity', fontsize=16, 
             fontweight='bold', color='black', pad=20)
ax.set_xticks(x + width / 2)
ax.set_xticklabels(crosstab_religion_marriage.index, fontsize=11, color='black')
ax.legend(title='Marriage Type', fontsize=11, title_fontsize=12, frameon=True, 
          edgecolor='black')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Add total valid responses
ax.text(0.02, 0.98, f'Total Valid Responses: {len(df_valid)}', 
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        color='black')

plt.tight_layout()
plt.savefig('6_religion_vs_marriage.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 6_religion_vs_marriage.png")

print(crosstab_religion_marriage)
print(f"\nTotal Valid: {len(df_valid)}")
print("\n" + "="*60 + "\n")

# ===================================================================
# ANALYSIS 7: Three-way Relationship (Heatmap)
# ===================================================================
print("ANALYSIS 7: Three-way Relationship (Socioeconomic, Religion, Marriage)")
print("-" * 60)

# Create multi-index crosstab
threeway = df_valid.groupby(['socioeconomic_class', 'religion', 
                             'marriage_consanguineous']).size().reset_index(name='count')

# Create separate heatmaps for Yes and No marriage types
for marriage_type in ['Yes', 'No']:
    data_subset = threeway[threeway['marriage_consanguineous'] == marriage_type]
    
    if len(data_subset) > 0:
        pivot_table = data_subset.pivot(index='religion', 
                                        columns='socioeconomic_class', 
                                        values='count').fillna(0)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create heatmap
        im = ax.imshow(pivot_table.values, cmap='YlOrRd', aspect='auto')
        
        # Set ticks
        ax.set_xticks(np.arange(len(pivot_table.columns)))
        ax.set_yticks(np.arange(len(pivot_table.index)))
        ax.set_xticklabels([f'Class {int(c)}' for c in pivot_table.columns], 
                          fontsize=12, color='black')
        ax.set_yticklabels(pivot_table.index, fontsize=12, color='black')
        
        # Add text annotations with counts and percentages
        for i in range(len(pivot_table.index)):
            for j in range(len(pivot_table.columns)):
                count = int(pivot_table.iloc[i, j])
                if count > 0:
                    total = pivot_table.iloc[i].sum()
                    percentage = (count / total * 100) if total > 0 else 0
                    text = ax.text(j, i, f'{count}\n({percentage:.1f}%)',
                                 ha="center", va="center", fontsize=10, 
                                 fontweight='bold', color='black')
        
        # Labels and title
        ax.set_xlabel('Socioeconomic Class', fontsize=14, fontweight='bold', color='black')
        ax.set_ylabel('Religion', fontsize=14, fontweight='bold', color='black')
        ax.set_title(f'Socioeconomic Class vs Religion\n(Marriage Consanguineous: {marriage_type})', 
                    fontsize=16, fontweight='bold', color='black', pad=20)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Count', fontsize=12, fontweight='bold', color='black')
        cbar.ax.tick_params(labelsize=10, colors='black')
        
        # Add total valid responses
        total_for_type = data_subset['count'].sum()
        ax.text(0.02, 1.08, f'Total Valid Responses: {int(total_for_type)}', 
                transform=ax.transAxes, fontsize=11, fontweight='bold',
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                color='black')
        
        plt.tight_layout()
        plt.savefig(f'7_threeway_heatmap_{marriage_type.lower()}.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Saved: 7_threeway_heatmap_{marriage_type.lower()}.png")

print("\n" + "="*60 + "\n")
print("All analyses completed successfully!")
print(f"\nSummary:")
print(f"- Total records in dataset: {len(df)}")
print(f"- Valid records analyzed: {len(df_valid)}")
print(f"- Missing/Invalid records: {len(df) - len(df_valid)}")
print(f"- Generated 8 visualization files")
