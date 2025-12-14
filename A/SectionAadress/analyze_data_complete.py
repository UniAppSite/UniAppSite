import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import os
warnings.filterwarnings('ignore')

# Create output directory for images
output_dir = 'analysis_outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}\n")

# Read the CSV file
df = pd.read_csv('Data.csv')

# Rename columns for easier handling
df.columns = ['Consanguineous_Marriage', 'Socioeconomic_Class', 'Location_Type', 'Spouse_Relation', 'Education_Level']

# Remove completely empty rows
df = df.dropna(how='all')

# Clean the data - remove extra whitespace and newlines
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df = df.apply(lambda x: x.str.replace('\n', '') if x.dtype == "object" else x)

# Standardize education data
df['Education_Level'] = df['Education_Level'].replace({
    'Secondary school': 'Secondary School', 
    'secondary school': 'Secondary School'
})

# Calculate total valid responses
total_valid_responses = len(df)

# Location mapping
location_map = {'R': 'Rural', 'S': 'Semi-urban', 'U': 'Urban'}

print("="*80)
print(f"TOTAL VALID RESPONSES: {total_valid_responses}")
print("="*80)
print("\n")

# =============================================================================
# IMAGE 1: BASIC DISTRIBUTIONS
# =============================================================================
print("Generating Image 1: Basic Distributions...")

fig1 = plt.figure(figsize=(16, 12))
fig1.suptitle(f'Basic Data Analysis\nTotal Valid Responses: {total_valid_responses}', 
             fontsize=16, fontweight='bold', color='black')

# 1. Consanguineous Marriage
ax1 = plt.subplot(2, 3, 1)
consang_data = df['Consanguineous_Marriage'].dropna()
consang_counts = consang_data.value_counts()
consang_percentages = (consang_counts / len(consang_data) * 100)

bars1 = ax1.bar(range(len(consang_counts)), consang_counts.values, 
                color=['#3498db', '#e74c3c'], edgecolor='black', linewidth=1.5)
ax1.set_xticks(range(len(consang_counts)))
ax1.set_xticklabels(consang_counts.index, color='black', fontweight='bold', fontsize=11)
ax1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax1.set_title('Consanguineous Marriage', fontweight='bold', color='black', fontsize=12)
ax1.tick_params(colors='black')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars1, consang_counts.values, consang_percentages.values):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

# 2. Socioeconomic Class
ax2 = plt.subplot(2, 3, 2)
socio_data = df['Socioeconomic_Class'].dropna()
socio_counts = socio_data.value_counts().sort_index()
socio_percentages = (socio_counts / len(socio_data) * 100)

colors = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71']
bars2 = ax2.bar(range(len(socio_counts)), socio_counts.values, 
                color=colors[:len(socio_counts)], edgecolor='black', linewidth=1.5)
ax2.set_xticks(range(len(socio_counts)))
ax2.set_xticklabels([f'Class {x}' for x in socio_counts.index], 
                     color='black', fontweight='bold', fontsize=10)
ax2.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax2.set_title('Socioeconomic Class', fontweight='bold', color='black', fontsize=12)
ax2.tick_params(colors='black')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars2, socio_counts.values, socio_percentages.values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=9)

# 3. Location Type
ax3 = plt.subplot(2, 3, 3)
location_data = df['Location_Type'].dropna()
location_data = location_data[location_data != '']
location_counts = location_data.value_counts()
location_percentages = (location_counts / len(location_data) * 100)

location_labels = [location_map.get(x, x) for x in location_counts.index]
colors_loc = ['#27ae60', '#f39c12', '#9b59b6']
bars3 = ax3.bar(range(len(location_counts)), location_counts.values, 
                color=colors_loc[:len(location_counts)], edgecolor='black', linewidth=1.5)
ax3.set_xticks(range(len(location_counts)))
ax3.set_xticklabels(location_labels, color='black', fontweight='bold', fontsize=11)
ax3.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax3.set_title('Location Type', fontweight='bold', color='black', fontsize=12)
ax3.tick_params(colors='black')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars3, location_counts.values, location_percentages.values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

# 4. Spouse Relation Degree
ax4 = plt.subplot(2, 3, 4)
relation_data = df[df['Consanguineous_Marriage'] == 'Yes']['Spouse_Relation'].dropna()
relation_data = relation_data[(relation_data != 'None') & (relation_data != '')]
relation_counts = relation_data.value_counts()
relation_percentages = (relation_counts / len(relation_data) * 100)

colors_rel = ['#e74c3c', '#3498db', '#2ecc71']
bars4 = ax4.bar(range(len(relation_counts)), relation_counts.values, 
                color=colors_rel[:len(relation_counts)], edgecolor='black', linewidth=1.5)
ax4.set_xticks(range(len(relation_counts)))
ax4.set_xticklabels(relation_counts.index, color='black', fontweight='bold', fontsize=10)
ax4.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax4.set_title('Spouse Relation Degree\n(Consanguineous Marriages)', 
              fontweight='bold', color='black', fontsize=12)
ax4.tick_params(colors='black')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.grid(axis='y', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars4, relation_counts.values, relation_percentages.values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}\n({pct:.1f}%)',
             ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

# 5. Education Level
ax5 = plt.subplot(2, 3, 5)
education_data = df['Education_Level'].dropna()
education_counts = education_data.value_counts()
education_percentages = (education_counts / len(education_data) * 100)

colors_edu = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71']
bars5 = ax5.barh(range(len(education_counts)), education_counts.values, 
                color=colors_edu[:len(education_counts)], edgecolor='black', linewidth=1.5)
ax5.set_yticks(range(len(education_counts)))
ax5.set_yticklabels(education_counts.index, color='black', fontweight='bold', fontsize=9)
ax5.set_xlabel('Count', fontweight='bold', color='black', fontsize=11)
ax5.set_title('Education Level Distribution', fontweight='bold', color='black', fontsize=12)
ax5.tick_params(colors='black')
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
ax5.grid(axis='x', alpha=0.3, linestyle='--')

for bar, count, pct in zip(bars5, education_counts.values, education_percentages.values):
    width = bar.get_width()
    ax5.text(width, bar.get_y() + bar.get_height()/2.,
             f' {int(count)} ({pct:.1f}%)',
             ha='left', va='center', fontweight='bold', color='black', fontsize=9)

# 6. Missing Data
ax6 = plt.subplot(2, 3, 6)
missing_counts = df.isnull().sum()
missing_counts = missing_counts[missing_counts > 0]
missing_percentages = (missing_counts / total_valid_responses * 100)

if len(missing_counts) > 0:
    bars6 = ax6.barh(range(len(missing_counts)), missing_counts.values, 
                     color='#e74c3c', edgecolor='black', linewidth=1.5)
    ax6.set_yticks(range(len(missing_counts)))
    col_labels = [col.replace('_', ' ') for col in missing_counts.index]
    ax6.set_yticklabels(col_labels, color='black', fontweight='bold', fontsize=9)
    ax6.set_xlabel('Missing Count', fontweight='bold', color='black', fontsize=11)
    ax6.set_title('Missing Data Analysis', fontweight='bold', color='black', fontsize=12)
    ax6.tick_params(colors='black')
    ax6.spines['top'].set_visible(False)
    ax6.spines['right'].set_visible(False)
    ax6.grid(axis='x', alpha=0.3, linestyle='--')
    
    for bar, count, pct in zip(bars6, missing_counts.values, missing_percentages.values):
        width = bar.get_width()
        ax6.text(width, bar.get_y() + bar.get_height()/2.,
                 f' {int(count)} ({pct:.1f}%)',
                 ha='left', va='center', fontweight='bold', color='black', fontsize=9)
else:
    ax6.text(0.5, 0.5, 'No Missing Data', ha='center', va='center', 
             fontsize=14, fontweight='bold', color='black')
    ax6.axis('off')

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_1 = os.path.join(output_dir, '01_basic_distributions.png')
plt.savefig(output_file_1, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_1}\n")
plt.close()

# =============================================================================
# IMAGE 2: LOCATION VS EDUCATION COMPARISON
# =============================================================================
print("Generating Image 2: Location vs Education...")

fig2 = plt.figure(figsize=(14, 6))
fig2.suptitle(f'Location vs Education Analysis\nTotal Valid Responses: {total_valid_responses}', 
             fontsize=14, fontweight='bold', color='black')

df_loc_edu = df.dropna(subset=['Location_Type', 'Education_Level'])
df_loc_edu = df_loc_edu[df_loc_edu['Location_Type'] != '']

if len(df_loc_edu) > 0:
    # Left: Grouped bar chart
    ax_le1 = plt.subplot(1, 2, 1)
    crosstab_loc_edu = pd.crosstab(df_loc_edu['Education_Level'], df_loc_edu['Location_Type'])
    crosstab_loc_edu = crosstab_loc_edu[[x for x in ['R', 'S', 'U'] if x in crosstab_loc_edu.columns]]
    
    x_pos = np.arange(len(crosstab_loc_edu.index))
    width = 0.25
    colors_loc = ['#27ae60', '#f39c12', '#9b59b6']
    
    for i, (loc_code, color) in enumerate(zip(crosstab_loc_edu.columns, colors_loc)):
        offset = (i - 1) * width
        loc_name = location_map.get(loc_code, loc_code)
        bars = ax_le1.bar(x_pos + offset, crosstab_loc_edu[loc_code], width, 
                         label=loc_name, color=color, edgecolor='black', linewidth=1.2)
        
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_le1.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}',
                           ha='center', va='bottom', fontweight='bold', color='black', fontsize=8)
    
    ax_le1.set_xlabel('Education Level', fontweight='bold', color='black', fontsize=11)
    ax_le1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
    ax_le1.set_title('Education by Location Type', fontweight='bold', color='black', fontsize=12)
    ax_le1.set_xticks(x_pos)
    ax_le1.set_xticklabels(crosstab_loc_edu.index, rotation=45, ha='right',
                           color='black', fontweight='bold', fontsize=9)
    ax_le1.legend(frameon=True, loc='upper right', fontsize=10)
    ax_le1.tick_params(colors='black')
    ax_le1.grid(axis='y', alpha=0.3, linestyle='--')
    ax_le1.spines['top'].set_visible(False)
    ax_le1.spines['right'].set_visible(False)
    
    # Right: Stacked percentage
    ax_le2 = plt.subplot(1, 2, 2)
    crosstab_loc_edu_pct = crosstab_loc_edu.div(crosstab_loc_edu.sum(axis=1), axis=0) * 100
    
    bottom_vals = np.zeros(len(crosstab_loc_edu_pct.index))
    
    for i, (loc_code, color) in enumerate(zip(crosstab_loc_edu_pct.columns, colors_loc)):
        loc_name = location_map.get(loc_code, loc_code)
        values = crosstab_loc_edu_pct[loc_code].values
        bars = ax_le2.barh(range(len(crosstab_loc_edu_pct.index)), values, 
                          left=bottom_vals, label=loc_name,
                          color=color, edgecolor='black', linewidth=1.2)
        
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 5:
                ax_le2.text(bottom_vals[j] + val/2., bar.get_y() + bar.get_height()/2.,
                           f'{val:.1f}%',
                           ha='center', va='center', fontweight='bold', 
                           color='black', fontsize=8)
        
        bottom_vals += values
    
    ax_le2.set_xlabel('Percentage (%)', fontweight='bold', color='black', fontsize=11)
    ax_le2.set_title('Education Distribution % by Location', fontweight='bold', color='black', fontsize=12)
    ax_le2.set_yticks(range(len(crosstab_loc_edu_pct.index)))
    ax_le2.set_yticklabels(crosstab_loc_edu_pct.index, color='black', fontweight='bold', fontsize=9)
    ax_le2.legend(frameon=True, loc='lower right', fontsize=10)
    ax_le2.tick_params(colors='black')
    ax_le2.grid(axis='x', alpha=0.3, linestyle='--')
    ax_le2.spines['top'].set_visible(False)
    ax_le2.spines['right'].set_visible(False)
    ax_le2.set_xlim(0, 100)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_2 = os.path.join(output_dir, '02_location_vs_education.png')
plt.savefig(output_file_2, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_2}\n")
plt.close()

# =============================================================================
# IMAGE 3: LOCATION VS EDUCATION VS CONSANGUINITY
# =============================================================================
print("Generating Image 3: Location vs Education vs Consanguinity...")

fig3 = plt.figure(figsize=(16, 10))
fig3.suptitle(f'Location vs Education vs Consanguinity Analysis\nTotal Valid Responses: {total_valid_responses}', 
             fontsize=14, fontweight='bold', color='black')

df_triple = df.dropna(subset=['Location_Type', 'Education_Level', 'Consanguineous_Marriage'])
df_triple = df_triple[df_triple['Location_Type'] != '']

if len(df_triple) > 0:
    df_yes = df_triple[df_triple['Consanguineous_Marriage'] == 'Yes']
    df_no = df_triple[df_triple['Consanguineous_Marriage'] == 'No']
    
    # Plot 1: Consanguineous=Yes
    ax_t1 = plt.subplot(2, 2, 1)
    if len(df_yes) > 0:
        ct_yes = pd.crosstab(df_yes['Education_Level'], df_yes['Location_Type'])
        ct_yes = ct_yes[[x for x in ['R', 'S', 'U'] if x in ct_yes.columns]]
        
        x_pos = np.arange(len(ct_yes.index))
        width = 0.25
        
        for i, (loc_code, color) in enumerate(zip(ct_yes.columns, colors_loc[:len(ct_yes.columns)])):
            offset = (i - len(ct_yes.columns)/2 + 0.5) * width
            loc_name = location_map.get(loc_code, loc_code)
            bars = ax_t1.bar(x_pos + offset, ct_yes[loc_code], width, 
                            label=loc_name, color=color, edgecolor='black', linewidth=1.2)
            
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax_t1.text(bar.get_x() + bar.get_width()/2., height,
                              f'{int(height)}',
                              ha='center', va='bottom', fontweight='bold', color='black', fontsize=7)
        
        ax_t1.set_ylabel('Count', fontweight='bold', color='black', fontsize=10)
        ax_t1.set_title('Consanguineous=YES\nEducation by Location', 
                       fontweight='bold', color='black', fontsize=11)
        ax_t1.set_xticks(x_pos)
        ax_t1.set_xticklabels(ct_yes.index, rotation=45, ha='right',
                             color='black', fontweight='bold', fontsize=8)
        ax_t1.legend(frameon=True, fontsize=8)
        ax_t1.tick_params(colors='black')
        ax_t1.grid(axis='y', alpha=0.3, linestyle='--')
        ax_t1.spines['top'].set_visible(False)
        ax_t1.spines['right'].set_visible(False)
    
    # Plot 2: Consanguineous=No
    ax_t2 = plt.subplot(2, 2, 2)
    if len(df_no) > 0:
        ct_no = pd.crosstab(df_no['Education_Level'], df_no['Location_Type'])
        ct_no = ct_no[[x for x in ['R', 'S', 'U'] if x in ct_no.columns]]
        
        x_pos = np.arange(len(ct_no.index))
        width = 0.25
        
        for i, (loc_code, color) in enumerate(zip(ct_no.columns, colors_loc[:len(ct_no.columns)])):
            offset = (i - len(ct_no.columns)/2 + 0.5) * width
            loc_name = location_map.get(loc_code, loc_code)
            bars = ax_t2.bar(x_pos + offset, ct_no[loc_code], width, 
                            label=loc_name, color=color, edgecolor='black', linewidth=1.2)
            
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax_t2.text(bar.get_x() + bar.get_width()/2., height,
                              f'{int(height)}',
                              ha='center', va='bottom', fontweight='bold', color='black', fontsize=7)
        
        ax_t2.set_ylabel('Count', fontweight='bold', color='black', fontsize=10)
        ax_t2.set_title('Consanguineous=NO\nEducation by Location', 
                       fontweight='bold', color='black', fontsize=11)
        ax_t2.set_xticks(x_pos)
        ax_t2.set_xticklabels(ct_no.index, rotation=45, ha='right',
                             color='black', fontweight='bold', fontsize=8)
        ax_t2.legend(frameon=True, fontsize=8)
        ax_t2.tick_params(colors='black')
        ax_t2.grid(axis='y', alpha=0.3, linestyle='--')
        ax_t2.spines['top'].set_visible(False)
        ax_t2.spines['right'].set_visible(False)
    
    # Plot 3: Consanguinity Rate by Education
    ax_t3 = plt.subplot(2, 2, 3)
    ct_edu_consang = pd.crosstab(df_triple['Education_Level'], df_triple['Consanguineous_Marriage'])
    
    if 'Yes' in ct_edu_consang.columns:
        consang_rate_edu = (ct_edu_consang['Yes'] / ct_edu_consang.sum(axis=1) * 100).sort_values(ascending=False)
        
        bars_t3 = ax_t3.barh(range(len(consang_rate_edu)), consang_rate_edu.values,
                            color='#e74c3c', edgecolor='black', linewidth=1.5)
        ax_t3.set_yticks(range(len(consang_rate_edu)))
        ax_t3.set_yticklabels(consang_rate_edu.index, color='black', fontweight='bold', fontsize=9)
        ax_t3.set_xlabel('Consanguineous Marriage Rate (%)', fontweight='bold', color='black', fontsize=10)
        ax_t3.set_title('Consanguinity Rate by Education', fontweight='bold', color='black', fontsize=11)
        ax_t3.tick_params(colors='black')
        ax_t3.grid(axis='x', alpha=0.3, linestyle='--')
        ax_t3.spines['top'].set_visible(False)
        ax_t3.spines['right'].set_visible(False)
        ax_t3.set_xlim(0, 100)
        
        for bar, rate in zip(bars_t3, consang_rate_edu.values):
            width = bar.get_width()
            ax_t3.text(width, bar.get_y() + bar.get_height()/2.,
                      f' {rate:.1f}%',
                      ha='left', va='center', fontweight='bold', color='black', fontsize=9)
    
    # Plot 4: Consanguinity Rate by Location
    ax_t4 = plt.subplot(2, 2, 4)
    ct_loc_consang = pd.crosstab(df_triple['Location_Type'], df_triple['Consanguineous_Marriage'])
    ct_loc_consang = ct_loc_consang.reindex([x for x in ['R', 'S', 'U'] if x in ct_loc_consang.index])
    
    if 'Yes' in ct_loc_consang.columns:
        consang_rate_loc = (ct_loc_consang['Yes'] / ct_loc_consang.sum(axis=1) * 100)
        loc_labels_t4 = [location_map.get(x, x) for x in consang_rate_loc.index]
        
        bars_t4 = ax_t4.bar(range(len(consang_rate_loc)), consang_rate_loc.values,
                           color=['#27ae60', '#f39c12', '#9b59b6'][:len(consang_rate_loc)], 
                           edgecolor='black', linewidth=1.5)
        ax_t4.set_xticks(range(len(consang_rate_loc)))
        ax_t4.set_xticklabels(loc_labels_t4, color='black', fontweight='bold', fontsize=10)
        ax_t4.set_ylabel('Consanguineous Marriage Rate (%)', fontweight='bold', color='black', fontsize=10)
        ax_t4.set_title('Consanguinity Rate by Location', fontweight='bold', color='black', fontsize=11)
        ax_t4.tick_params(colors='black')
        ax_t4.grid(axis='y', alpha=0.3, linestyle='--')
        ax_t4.spines['top'].set_visible(False)
        ax_t4.spines['right'].set_visible(False)
        ax_t4.set_ylim(0, 100)
        
        for bar, rate in zip(bars_t4, consang_rate_loc.values):
            height = bar.get_height()
            ax_t4.text(bar.get_x() + bar.get_width()/2., height,
                      f'{rate:.1f}%',
                      ha='center', va='bottom', fontweight='bold', color='black', fontsize=10)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_3 = os.path.join(output_dir, '03_location_education_consanguinity.png')
plt.savefig(output_file_3, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_3}\n")
plt.close()

# =============================================================================
# IMAGE 4: ADDITIONAL COMPARATIVE ANALYSIS
# =============================================================================
print("Generating Image 4: Additional Comparative Analysis...")

fig4 = plt.figure(figsize=(16, 6))
fig4.suptitle(f'Comparative Analysis: Consanguinity by Demographics\nTotal Valid Responses: {total_valid_responses}', 
             fontsize=14, fontweight='bold', color='black')

# Plot 1: Consanguineous Marriage by Location
ax_c1 = plt.subplot(1, 3, 1)
df_clean = df.dropna(subset=['Consanguineous_Marriage', 'Location_Type'])
df_clean = df_clean[df_clean['Location_Type'] != '']
crosstab_loc = pd.crosstab(df_clean['Location_Type'], df_clean['Consanguineous_Marriage'])
crosstab_loc = crosstab_loc.reindex([x for x in ['R', 'S', 'U'] if x in crosstab_loc.index])
location_labels_full = [location_map.get(x, x) for x in crosstab_loc.index]

x_pos = np.arange(len(crosstab_loc.index))
width = 0.35

if 'Yes' in crosstab_loc.columns and 'No' in crosstab_loc.columns:
    bars_yes = ax_c1.bar(x_pos - width/2, crosstab_loc['Yes'], width, 
                         label='Yes', color='#e74c3c', edgecolor='black', linewidth=1.5)
    bars_no = ax_c1.bar(x_pos + width/2, crosstab_loc['No'], width, 
                        label='No', color='#3498db', edgecolor='black', linewidth=1.5)
    
    for bars in [bars_yes, bars_no]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax_c1.text(bar.get_x() + bar.get_width()/2., height,
                          f'{int(height)}',
                          ha='center', va='bottom', fontweight='bold', color='black', fontsize=9)

ax_c1.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=11)
ax_c1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
ax_c1.set_title('Consanguineous Marriage by Location', fontweight='bold', color='black', fontsize=12)
ax_c1.set_xticks(x_pos)
ax_c1.set_xticklabels(location_labels_full, color='black', fontweight='bold', fontsize=10)
ax_c1.legend(frameon=True, loc='upper right', fontsize=10)
ax_c1.tick_params(colors='black')
ax_c1.grid(axis='y', alpha=0.3, linestyle='--')
ax_c1.spines['top'].set_visible(False)
ax_c1.spines['right'].set_visible(False)

# Plot 2: Consanguineous Marriage by Socioeconomic Class
ax_c2 = plt.subplot(1, 3, 2)
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
ax_c2.set_title('Consanguineous Marriage by Class', fontweight='bold', color='black', fontsize=12)
ax_c2.set_xticks(x_pos2)
ax_c2.set_xticklabels([f'Class {x}' for x in crosstab_socio.index], 
                       color='black', fontweight='bold', fontsize=10)
ax_c2.legend(frameon=True, loc='upper right', fontsize=10)
ax_c2.tick_params(colors='black')
ax_c2.grid(axis='y', alpha=0.3, linestyle='--')
ax_c2.spines['top'].set_visible(False)
ax_c2.spines['right'].set_visible(False)

# Plot 3: Socioeconomic Class by Location (Stacked)
ax_c3 = plt.subplot(1, 3, 3)
df_clean3 = df.dropna(subset=['Location_Type', 'Socioeconomic_Class'])
df_clean3 = df_clean3[df_clean3['Location_Type'] != '']
crosstab_loc_socio = pd.crosstab(df_clean3['Location_Type'], df_clean3['Socioeconomic_Class'])
crosstab_loc_socio = crosstab_loc_socio.reindex([x for x in ['R', 'S', 'U'] if x in crosstab_loc_socio.index])
location_labels_full2 = [location_map.get(x, x) for x in crosstab_loc_socio.index]

colors_stack = ['#e74c3c', '#e67e22', '#f39c12', '#3498db', '#2ecc71']
bottom_vals = np.zeros(len(crosstab_loc_socio.index))

for i, col in enumerate(sorted(crosstab_loc_socio.columns)):
    values = crosstab_loc_socio[col].values
    bars = ax_c3.bar(range(len(crosstab_loc_socio.index)), values, 
                     bottom=bottom_vals, label=f'Class {col}',
                     color=colors_stack[i % len(colors_stack)], 
                     edgecolor='black', linewidth=1.2)
    
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
ax_c3.set_title('Socioeconomic Class by Location', fontweight='bold', color='black', fontsize=12)
ax_c3.set_xticks(range(len(crosstab_loc_socio.index)))
ax_c3.set_xticklabels(location_labels_full2, color='black', fontweight='bold', fontsize=10)
ax_c3.legend(frameon=True, loc='upper right', fontsize=9)
ax_c3.tick_params(colors='black')
ax_c3.grid(axis='y', alpha=0.3, linestyle='--')
ax_c3.spines['top'].set_visible(False)
ax_c3.spines['right'].set_visible(False)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_4 = os.path.join(output_dir, '04_comparative_demographics.png')
plt.savefig(output_file_4, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_4}\n")
plt.close()

# =============================================================================
# IMAGE 5: LOCATION VS EDUCATION VS SOCIOECONOMIC CLASS
# =============================================================================
print("Generating Image 5: Location vs Education vs Socioeconomic Class...")

fig5 = plt.figure(figsize=(18, 12))
fig5.suptitle(f'Location vs Education vs Socioeconomic Class Analysis\nTotal Valid Responses: {total_valid_responses}', 
             fontsize=15, fontweight='bold', color='black')

# Filter data for triple analysis
df_triple_class = df.dropna(subset=['Location_Type', 'Education_Level', 'Socioeconomic_Class'])
df_triple_class = df_triple_class[df_triple_class['Location_Type'] != '']

if len(df_triple_class) > 0:
    # Define colors for socioeconomic classes
    class_colors = {1: '#e74c3c', 2: '#e67e22', 3: '#f39c12', 4: '#3498db', 5: '#2ecc71'}
    
    # Plot 1: Education Distribution by Location (OVERALL - All Classes)
    ax_5_1 = plt.subplot(2, 3, 1)
    
    ct_loc_edu_overall = pd.crosstab(df_triple_class['Location_Type'], df_triple_class['Education_Level'])
    ct_loc_edu_overall = ct_loc_edu_overall.reindex([x for x in ['R', 'S', 'U'] if x in ct_loc_edu_overall.index])
    
    # Get top 4 education levels
    top_edu_levels = df_triple_class['Education_Level'].value_counts().head(4).index
    ct_loc_edu_overall = ct_loc_edu_overall[[col for col in top_edu_levels if col in ct_loc_edu_overall.columns]]
    
    x_pos = np.arange(len(ct_loc_edu_overall.index))
    width = 0.2
    loc_labels = [location_map.get(x, x) for x in ct_loc_edu_overall.index]
    
    edu_colors_map = {'Secondary School': '#3498db', 'Graduate': '#2ecc71', 
                      'Primary School': '#f39c12', 'No formal education': '#e74c3c',
                      'Postgraduate': '#9b59b6'}
    
    for i, edu in enumerate(ct_loc_edu_overall.columns):
        offset = (i - len(ct_loc_edu_overall.columns)/2 + 0.5) * width
        values = ct_loc_edu_overall[edu].values
        bars = ax_5_1.bar(x_pos + offset, values, width, 
                         label=edu[:15],
                         color=edu_colors_map.get(edu, '#95a5a6'), 
                         edgecolor='black', linewidth=1.2)
        
        for bar, val in zip(bars, values):
            if val > 0:
                ax_5_1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                           f'{int(val)}',
                           ha='center', va='bottom', fontweight='bold', 
                           color='black', fontsize=7)
    
    ax_5_1.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=10)
    ax_5_1.set_ylabel('Count', fontweight='bold', color='black', fontsize=10)
    ax_5_1.set_title('Education by Location\n(OVERALL - Top 4 Levels)', 
                    fontweight='bold', color='black', fontsize=11)
    ax_5_1.set_xticks(x_pos)
    ax_5_1.set_xticklabels(loc_labels, color='black', fontweight='bold', fontsize=10)
    ax_5_1.legend(frameon=True, fontsize=7, loc='upper right')
    ax_5_1.tick_params(colors='black')
    ax_5_1.grid(axis='y', alpha=0.3, linestyle='--')
    ax_5_1.spines['top'].set_visible(False)
    ax_5_1.spines['right'].set_visible(False)
    
    # Plot 2: Socioeconomic Class Distribution by Location
    ax_5_2 = plt.subplot(2, 3, 2)
    ct_loc_class = pd.crosstab(df_triple_class['Location_Type'], df_triple_class['Socioeconomic_Class'])
    ct_loc_class = ct_loc_class.reindex([x for x in ['R', 'S', 'U'] if x in ct_loc_class.index])
    
    # Stacked bar chart
    bottom = np.zeros(len(ct_loc_class.index))
    loc_labels_2 = [location_map.get(x, x) for x in ct_loc_class.index]
    
    for class_num in sorted(ct_loc_class.columns):
        values = ct_loc_class[class_num].values
        bars = ax_5_2.bar(range(len(ct_loc_class.index)), values, 
                         bottom=bottom, label=f'Class {class_num}',
                         color=class_colors.get(class_num, '#95a5a6'), 
                         edgecolor='black', linewidth=1.2)
        
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 3:  # Only show label if count > 3
                ax_5_2.text(bar.get_x() + bar.get_width()/2., 
                           bottom[j] + val/2.,
                           f'{int(val)}',
                           ha='center', va='center', fontweight='bold', 
                           color='white', fontsize=8,
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.6))
        
        bottom += values
    
    ax_5_2.set_ylabel('Count', fontweight='bold', color='black', fontsize=10)
    ax_5_2.set_title('Socioeconomic Class by Location\n(Stacked)', 
                    fontweight='bold', color='black', fontsize=11)
    ax_5_2.set_xticks(range(len(ct_loc_class.index)))
    ax_5_2.set_xticklabels(loc_labels_2, color='black', fontweight='bold', fontsize=10)
    ax_5_2.legend(frameon=True, fontsize=8, loc='upper right')
    ax_5_2.tick_params(colors='black')
    ax_5_2.grid(axis='y', alpha=0.3, linestyle='--')
    ax_5_2.spines['top'].set_visible(False)
    ax_5_2.spines['right'].set_visible(False)
    
    # Plot 3: Education Distribution by Socioeconomic Class
    ax_5_3 = plt.subplot(2, 3, 3)
    ct_class_edu = pd.crosstab(df_triple_class['Socioeconomic_Class'], df_triple_class['Education_Level'])
    
    x_pos_3 = np.arange(len(ct_class_edu.index))
    width_3 = 0.18
    
    # Get top 4 education levels
    top_edu = df_triple_class['Education_Level'].value_counts().head(4).index
    edu_colors_map = {'Secondary School': '#3498db', 'Graduate': '#2ecc71', 
                      'Primary School': '#f39c12', 'No formal education': '#e74c3c',
                      'Postgraduate': '#9b59b6'}
    
    for i, edu in enumerate(top_edu):
        if edu in ct_class_edu.columns:
            offset = (i - len(top_edu)/2 + 0.5) * width_3
            values = ct_class_edu[edu].values
            bars = ax_5_3.bar(x_pos_3 + offset, values, width_3, 
                             label=edu[:15], color=edu_colors_map.get(edu, '#95a5a6'),
                             edgecolor='black', linewidth=1.2)
            
            for bar, val in zip(bars, values):
                if val > 0:
                    ax_5_3.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                               f'{int(val)}',
                               ha='center', va='bottom', fontweight='bold', 
                               color='black', fontsize=7)
    
    ax_5_3.set_xlabel('Socioeconomic Class', fontweight='bold', color='black', fontsize=10)
    ax_5_3.set_ylabel('Count', fontweight='bold', color='black', fontsize=10)
    ax_5_3.set_title('Education by Socioeconomic Class\n(Top 4 Education Levels)', 
                    fontweight='bold', color='black', fontsize=11)
    ax_5_3.set_xticks(x_pos_3)
    ax_5_3.set_xticklabels([f'Class {x}' for x in ct_class_edu.index], 
                           color='black', fontweight='bold', fontsize=10)
    ax_5_3.legend(frameon=True, fontsize=7, loc='upper right')
    ax_5_3.tick_params(colors='black')
    ax_5_3.grid(axis='y', alpha=0.3, linestyle='--')
    ax_5_3.spines['top'].set_visible(False)
    ax_5_3.spines['right'].set_visible(False)
    
    # Plot 4: Socioeconomic Class Distribution by Location & Education (Stacked)
    ax_5_4 = plt.subplot(2, 3, 4)
    
    # Get top 3 education levels
    top_3_edu = df_triple_class['Education_Level'].value_counts().head(3).index
    df_edu_subset = df_triple_class[df_triple_class['Education_Level'].isin(top_3_edu)]
    
    if len(df_edu_subset) > 0:
        # Create crosstab for location and education
        loc_edu_combinations = []
        for loc in ['R', 'S', 'U']:
            for edu in top_3_edu:
                df_subset = df_edu_subset[(df_edu_subset['Location_Type'] == loc) & 
                                         (df_edu_subset['Education_Level'] == edu)]
                if len(df_subset) > 0:
                    loc_edu_combinations.append({
                        'Location': location_map.get(loc, loc),
                        'Education': edu[:10],
                        'Location_Code': loc,
                        'Education_Full': edu
                    })
        
        # For each location-education combo, stack the classes
        combo_labels = [f"{c['Location']}\n{c['Education']}" for c in loc_edu_combinations[:6]]  # Limit to 6
        x_pos_4 = np.arange(len(combo_labels))
        
        bottom = np.zeros(len(combo_labels))
        
        for class_num in sorted(df_triple_class['Socioeconomic_Class'].unique()):
            values = []
            for combo in loc_edu_combinations[:6]:
                df_subset = df_triple_class[
                    (df_triple_class['Location_Type'] == combo['Location_Code']) &
                    (df_triple_class['Education_Level'] == combo['Education_Full']) &
                    (df_triple_class['Socioeconomic_Class'] == class_num)
                ]
                values.append(len(df_subset))
            
            bars = ax_5_4.bar(x_pos_4, values, bottom=bottom, 
                            label=f'Class {class_num}',
                            color=class_colors.get(class_num, '#95a5a6'), 
                            edgecolor='black', linewidth=1.2)
            
            for j, (bar, val) in enumerate(zip(bars, values)):
                if val > 0:
                    ax_5_4.text(bar.get_x() + bar.get_width()/2., 
                               bottom[j] + val/2.,
                               f'{int(val)}',
                               ha='center', va='center', fontweight='bold', 
                               color='white', fontsize=7,
                               bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.6))
            
            bottom += values
        
        ax_5_4.set_ylabel('Count', fontweight='bold', color='black', fontsize=10)
        ax_5_4.set_title('Class Distribution by Location & Education\n(Top 3 Education Levels)', 
                        fontweight='bold', color='black', fontsize=11)
        ax_5_4.set_xticks(x_pos_4)
        ax_5_4.set_xticklabels(combo_labels, color='black', fontweight='bold', fontsize=7, rotation=0)
        ax_5_4.legend(frameon=True, fontsize=7, loc='upper right', ncol=2)
        ax_5_4.tick_params(colors='black')
        ax_5_4.grid(axis='y', alpha=0.3, linestyle='--')
        ax_5_4.spines['top'].set_visible(False)
        ax_5_4.spines['right'].set_visible(False)
    else:
        ax_5_4.text(0.5, 0.5, 'Insufficient Data', 
                   ha='center', va='center', fontsize=12, fontweight='bold', color='black')
        ax_5_4.axis('off')
    
    # Plot 5: Heatmap - OVERALL Location vs Education (All Classes Combined)
    ax_5_5 = plt.subplot(2, 3, 5)
    
    hm_overall = pd.crosstab(df_triple_class['Education_Level'], df_triple_class['Location_Type'])
    hm_overall = hm_overall[[x for x in ['R', 'S', 'U'] if x in hm_overall.columns]]
    
    # Sort by total count
    hm_overall['Total'] = hm_overall.sum(axis=1)
    hm_overall = hm_overall.sort_values('Total', ascending=False).drop('Total', axis=1)
    
    im = ax_5_5.imshow(hm_overall.values, cmap='RdYlGn', aspect='auto', interpolation='nearest')
    
    ax_5_5.set_xticks(range(len(hm_overall.columns)))
    ax_5_5.set_yticks(range(len(hm_overall.index)))
    ax_5_5.set_xticklabels([location_map.get(x, x) for x in hm_overall.columns], 
                           color='black', fontweight='bold', fontsize=10)
    ax_5_5.set_yticklabels(hm_overall.index, color='black', fontweight='bold', fontsize=8)
    ax_5_5.set_title('Heatmap: Education vs Location\n(OVERALL - All Classes)', 
                    fontweight='bold', color='black', fontsize=11)
    ax_5_5.tick_params(colors='black')
    
    # Add count annotations with percentages
    total_responses = hm_overall.values.sum()
    for i in range(len(hm_overall.index)):
        for j in range(len(hm_overall.columns)):
            count = hm_overall.iloc[i, j]
            pct = (count / total_responses * 100) if total_responses > 0 else 0
            ax_5_5.text(j, i, f'{int(count)}\n({pct:.1f}%)',
                       ha='center', va='center', color='black', 
                       fontweight='bold', fontsize=8)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax_5_5, fraction=0.046, pad=0.04)
    cbar.set_label('Count', rotation=270, labelpad=15, fontweight='bold', color='black')
    cbar.ax.tick_params(colors='black')
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax_5_5, fraction=0.046, pad=0.04)
    cbar.set_label('Count', rotation=270, labelpad=15, fontweight='bold', color='black')
    cbar.ax.tick_params(colors='black')
    
    # Plot 6: 3D-style Grouped Comparison - Location vs Class for each Education Level
    ax_5_6 = plt.subplot(2, 3, 6)
    
    # Get top 3 education levels
    top_3_edu_final = df_triple_class['Education_Level'].value_counts().head(3).index
    
    # Calculate average class for each location within each education level
    summary_data = []
    for edu in top_3_edu_final:
        for loc in ['R', 'S', 'U']:
            df_subset = df_triple_class[(df_triple_class['Education_Level'] == edu) & 
                                       (df_triple_class['Location_Type'] == loc)]
            if len(df_subset) > 0:
                avg_class = df_subset['Socioeconomic_Class'].mean()
                count = len(df_subset)
                summary_data.append({
                    'Education': edu[:12],
                    'Location': location_map.get(loc, loc),
                    'Avg_Class': avg_class,
                    'Count': count
                })
    
    if len(summary_data) > 0:
        summary_df = pd.DataFrame(summary_data)
        
        # Create grouped bar chart
        edu_unique = summary_df['Education'].unique()
        x_pos_6 = np.arange(len(edu_unique))
        width_6 = 0.25
        
        for i, loc in enumerate(['Rural', 'Semi-urban', 'Urban']):
            loc_data = summary_df[summary_df['Location'] == loc]
            # Align with education levels
            values = []
            counts = []
            for edu in edu_unique:
                edu_row = loc_data[loc_data['Education'] == edu]
                if len(edu_row) > 0:
                    values.append(edu_row['Avg_Class'].values[0])
                    counts.append(edu_row['Count'].values[0])
                else:
                    values.append(0)
                    counts.append(0)
            
            offset = (i - 1) * width_6
            bars = ax_5_6.bar(x_pos_6 + offset, values, width_6, 
                             label=loc, color=colors_loc[i],
                             edgecolor='black', linewidth=1.2)
            
            for bar, val, cnt in zip(bars, values, counts):
                if val > 0:
                    ax_5_6.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                               f'{val:.1f}\n(n={cnt})',
                               ha='center', va='bottom', fontweight='bold', 
                               color='black', fontsize=7)
        
        ax_5_6.set_xlabel('Education Level', fontweight='bold', color='black', fontsize=10)
        ax_5_6.set_ylabel('Average Socioeconomic Class', fontweight='bold', color='black', fontsize=10)
        ax_5_6.set_title('Avg Class by Location & Education\n(OVERALL - Top 3 Levels)', 
                        fontweight='bold', color='black', fontsize=11)
        ax_5_6.set_xticks(x_pos_6)
        ax_5_6.set_xticklabels(edu_unique, rotation=20, ha='right',
                               color='black', fontweight='bold', fontsize=8)
        ax_5_6.legend(frameon=True, fontsize=8, loc='upper right')
        ax_5_6.tick_params(colors='black')
        ax_5_6.grid(axis='y', alpha=0.3, linestyle='--')
        ax_5_6.spines['top'].set_visible(False)
        ax_5_6.spines['right'].set_visible(False)
        ax_5_6.set_ylim(0, 6)
        ax_5_6.axhline(y=3, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    else:
        ax_5_6.text(0.5, 0.5, 'Insufficient Data', 
                   ha='center', va='center', fontsize=12, fontweight='bold', color='black')
        ax_5_6.axis('off')
    
    # Print statistics
    print("\nLOCATION VS EDUCATION VS SOCIOECONOMIC CLASS:")
    print(f"Valid responses for triple analysis: {len(df_triple_class)}")
    print("\nCrosstab - Location vs Socioeconomic Class:")
    print(ct_loc_class)
    print("\nCrosstab - Socioeconomic Class vs Education:")
    print(ct_class_edu)
    print("\n")

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_5 = os.path.join(output_dir, '05_location_education_income_class.png')
plt.savefig(output_file_5, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_5}\n")
plt.close()

# =============================================================================
# INDIVIDUAL DETAILED IMAGES WITH CONSANGUINITY COMPARISON
# =============================================================================

# =============================================================================
# IMAGE 6: EDUCATION BY LOCATION (with Consanguinity Comparison)
# =============================================================================
print("Generating Image 6: Education by Location + Consanguinity...")

fig6 = plt.figure(figsize=(16, 6))

# Filter data
df_loc_edu_consang = df.dropna(subset=['Location_Type', 'Education_Level', 'Consanguineous_Marriage'])
df_loc_edu_consang = df_loc_edu_consang[df_loc_edu_consang['Location_Type'] != '']
total_valid_6 = len(df_loc_edu_consang)

fig6.suptitle(f'Education by Location with Consanguinity Comparison\nTotal Valid Responses: {total_valid_6}', 
             fontsize=14, fontweight='bold', color='black')

if len(df_loc_edu_consang) > 0:
    df_yes_6 = df_loc_edu_consang[df_loc_edu_consang['Consanguineous_Marriage'] == 'Yes']
    df_no_6 = df_loc_edu_consang[df_loc_edu_consang['Consanguineous_Marriage'] == 'No']
    
    # Left: Consanguineous = Yes
    ax_6_1 = plt.subplot(1, 2, 1)
    ct_yes = pd.crosstab(df_yes_6['Location_Type'], df_yes_6['Education_Level'])
    ct_yes = ct_yes.reindex([x for x in ['R', 'S', 'U'] if x in ct_yes.index])
    
    top_edu = df_loc_edu_consang['Education_Level'].value_counts().head(4).index
    ct_yes = ct_yes[[col for col in top_edu if col in ct_yes.columns]]
    
    x_pos = np.arange(len(ct_yes.index))
    width = 0.2
    loc_labels = [location_map.get(x, x) for x in ct_yes.index]
    
    edu_colors_map = {'Secondary School': '#3498db', 'Graduate': '#2ecc71', 
                      'Primary School': '#f39c12', 'No formal education': '#e74c3c',
                      'Postgraduate': '#9b59b6'}
    
    for i, edu in enumerate(ct_yes.columns):
        offset = (i - len(ct_yes.columns)/2 + 0.5) * width
        values = ct_yes[edu].values
        bars = ax_6_1.bar(x_pos + offset, values, width, 
                         label=edu[:15],
                         color=edu_colors_map.get(edu, '#95a5a6'), 
                         edgecolor='black', linewidth=1.2)
        
        for bar, val in zip(bars, values):
            if val > 0:
                ax_6_1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                           f'{int(val)}',
                           ha='center', va='bottom', fontweight='bold', 
                           color='black', fontsize=8)
    
    ax_6_1.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=11)
    ax_6_1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
    ax_6_1.set_title(f'Consanguineous = YES\n(n={len(df_yes_6)})', 
                    fontweight='bold', color='black', fontsize=12)
    ax_6_1.set_xticks(x_pos)
    ax_6_1.set_xticklabels(loc_labels, color='black', fontweight='bold', fontsize=10)
    ax_6_1.legend(frameon=True, fontsize=8, loc='upper right')
    ax_6_1.tick_params(colors='black')
    ax_6_1.grid(axis='y', alpha=0.3, linestyle='--')
    ax_6_1.spines['top'].set_visible(False)
    ax_6_1.spines['right'].set_visible(False)
    
    # Right: Consanguineous = No
    ax_6_2 = plt.subplot(1, 2, 2)
    ct_no = pd.crosstab(df_no_6['Location_Type'], df_no_6['Education_Level'])
    ct_no = ct_no.reindex([x for x in ['R', 'S', 'U'] if x in ct_no.index])
    ct_no = ct_no[[col for col in top_edu if col in ct_no.columns]]
    
    for i, edu in enumerate(ct_no.columns):
        offset = (i - len(ct_no.columns)/2 + 0.5) * width
        values = ct_no[edu].values
        bars = ax_6_2.bar(x_pos + offset, values, width, 
                         label=edu[:15],
                         color=edu_colors_map.get(edu, '#95a5a6'), 
                         edgecolor='black', linewidth=1.2)
        
        for bar, val in zip(bars, values):
            if val > 0:
                ax_6_2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                           f'{int(val)}',
                           ha='center', va='bottom', fontweight='bold', 
                           color='black', fontsize=8)
    
    ax_6_2.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=11)
    ax_6_2.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
    ax_6_2.set_title(f'Consanguineous = NO\n(n={len(df_no_6)})', 
                    fontweight='bold', color='black', fontsize=12)
    ax_6_2.set_xticks(x_pos)
    ax_6_2.set_xticklabels(loc_labels, color='black', fontweight='bold', fontsize=10)
    ax_6_2.legend(frameon=True, fontsize=8, loc='upper right')
    ax_6_2.tick_params(colors='black')
    ax_6_2.grid(axis='y', alpha=0.3, linestyle='--')
    ax_6_2.spines['top'].set_visible(False)
    ax_6_2.spines['right'].set_visible(False)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_6 = os.path.join(output_dir, '06_education_by_location_consanguinity.png')
plt.savefig(output_file_6, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_6}\n")
plt.close()

print("✓ Successfully generated Education by Location with Consanguinity comparison!")

# =============================================================================
# IMAGE 7: SOCIOECONOMIC CLASS BY LOCATION (with Consanguinity Comparison)
# =============================================================================
print("Generating Image 7: Socioeconomic Class by Location + Consanguinity...")

fig7 = plt.figure(figsize=(16, 6))

# Filter data
df_class_loc_consang = df.dropna(subset=['Location_Type', 'Socioeconomic_Class', 'Consanguineous_Marriage'])
df_class_loc_consang = df_class_loc_consang[df_class_loc_consang['Location_Type'] != '']
total_valid_7 = len(df_class_loc_consang)

fig7.suptitle(f'Socioeconomic Class by Location with Consanguinity Comparison\nTotal Valid Responses: {total_valid_7}', 
             fontsize=14, fontweight='bold', color='black')

if len(df_class_loc_consang) > 0:
    df_yes_7 = df_class_loc_consang[df_class_loc_consang['Consanguineous_Marriage'] == 'Yes']
    df_no_7 = df_class_loc_consang[df_class_loc_consang['Consanguineous_Marriage'] == 'No']
    
    class_colors = {1: '#3498db', 2: '#2ecc71', 3: '#f39c12', 4: '#e74c3c', 5: '#9b59b6'}
    
    # Left: Consanguineous = Yes
    ax_7_1 = plt.subplot(1, 2, 1)
    ct_yes = pd.crosstab(df_yes_7['Location_Type'], df_yes_7['Socioeconomic_Class'])
    ct_yes = ct_yes.reindex([x for x in ['R', 'S', 'U'] if x in ct_yes.index])
    
    x_pos = np.arange(len(ct_yes.index))
    bottom_yes = np.zeros(len(ct_yes.index))
    loc_labels = [location_map.get(x, x) for x in ct_yes.index]
    
    for class_num in sorted(ct_yes.columns):
        values = ct_yes[class_num].values
        bars = ax_7_1.bar(x_pos, values, bottom=bottom_yes,
                         label=f'Class {class_num}',
                         color=class_colors.get(class_num, '#95a5a6'),
                         edgecolor='black', linewidth=1.2)
        
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 2:
                ax_7_1.text(bar.get_x() + bar.get_width()/2.,
                           bottom_yes[j] + val/2.,
                           f'{int(val)}',
                           ha='center', va='center', fontweight='bold',
                           color='black', fontsize=9)
        
        bottom_yes += values
    
    ax_7_1.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=11)
    ax_7_1.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
    ax_7_1.set_title(f'Consanguineous = YES\n(n={len(df_yes_7)})', 
                    fontweight='bold', color='black', fontsize=12)
    ax_7_1.set_xticks(x_pos)
    ax_7_1.set_xticklabels(loc_labels, color='black', fontweight='bold', fontsize=10)
    ax_7_1.legend(frameon=True, fontsize=9, loc='upper right')
    ax_7_1.tick_params(colors='black')
    ax_7_1.grid(axis='y', alpha=0.3, linestyle='--')
    ax_7_1.spines['top'].set_visible(False)
    ax_7_1.spines['right'].set_visible(False)
    
    # Right: Consanguineous = No
    ax_7_2 = plt.subplot(1, 2, 2)
    ct_no = pd.crosstab(df_no_7['Location_Type'], df_no_7['Socioeconomic_Class'])
    ct_no = ct_no.reindex([x for x in ['R', 'S', 'U'] if x in ct_no.index])
    
    bottom_no = np.zeros(len(ct_no.index))
    
    for class_num in sorted(ct_no.columns):
        values = ct_no[class_num].values
        bars = ax_7_2.bar(x_pos, values, bottom=bottom_no,
                         label=f'Class {class_num}',
                         color=class_colors.get(class_num, '#95a5a6'),
                         edgecolor='black', linewidth=1.2)
        
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 2:
                ax_7_2.text(bar.get_x() + bar.get_width()/2.,
                           bottom_no[j] + val/2.,
                           f'{int(val)}',
                           ha='center', va='center', fontweight='bold',
                           color='black', fontsize=9)
        
        bottom_no += values
    
    ax_7_2.set_xlabel('Location Type', fontweight='bold', color='black', fontsize=11)
    ax_7_2.set_ylabel('Count', fontweight='bold', color='black', fontsize=11)
    ax_7_2.set_title(f'Consanguineous = NO\n(n={len(df_no_7)})', 
                    fontweight='bold', color='black', fontsize=12)
    ax_7_2.set_xticks(x_pos)
    ax_7_2.set_xticklabels(loc_labels, color='black', fontweight='bold', fontsize=10)
    ax_7_2.legend(frameon=True, fontsize=9, loc='upper right')
    ax_7_2.tick_params(colors='black')
    ax_7_2.grid(axis='y', alpha=0.3, linestyle='--')
    ax_7_2.spines['top'].set_visible(False)
    ax_7_2.spines['right'].set_visible(False)

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
output_file_7 = os.path.join(output_dir, '07_class_by_location_consanguinity.png')
plt.savefig(output_file_7, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Saved: {output_file_7}\n")
plt.close()

print("✓ Successfully generated Socioeconomic Class by Location with Consanguinity comparison!")
print("="*80)

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================
print("="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print(f"\nTotal Valid Responses: {total_valid_responses}")
print(f"\nGenerated Images:")
print(f"  1. {output_file_1}")
print(f"  2. {output_file_2}")
print(f"  3. {output_file_3}")
print(f"  4. {output_file_4}")
print(f"  5. {output_file_5}")
print(f"  6. {output_file_6}")
print(f"  7. {output_file_7}")
print("\n" + "="*80)
