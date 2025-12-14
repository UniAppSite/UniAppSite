import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data(filepath):
    """Load CSV data and handle missing values"""
    try:
        # Read CSV with proper column names
        df = pd.read_csv(filepath)
        
        # Rename columns for easier access
        df.columns = ['Sex', 'Type_Of_Disease', 'Religion', 'Consanguineous']
        
        # Strip whitespace from all string columns
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_disease_by_religion_chart(df):
    """Create bar chart for Disease Type Distribution by Religion"""
    # Remove rows with missing Disease or Religion data
    df_clean = df[df['Type_Of_Disease'].notna() & 
                  (df['Type_Of_Disease'] != '') & 
                  df['Religion'].notna() & 
                  (df['Religion'] != '')].copy()
    
    total_valid = len(df_clean)
    
    if total_valid == 0:
        print("No valid data for Disease Type by Religion")
        return
    
    # Create cross-tabulation
    cross_tab = pd.crosstab(df_clean['Type_Of_Disease'], df_clean['Religion'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Set position of bars
    x = np.arange(len(cross_tab.index))
    width = 0.25
    religions = cross_tab.columns
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    # Plot bars for each religion
    for i, religion in enumerate(religions):
        values = cross_tab[religion].values
        bars = ax.bar(x + i * width, values, width, 
                      label=religion, color=colors[i % len(colors)],
                      edgecolor='black', linewidth=1.2)
        
        # Add count and percentage labels on bars
        for j, (bar, val) in enumerate(zip(bars, values)):
            if val > 0:
                percentage = (val / total_valid) * 100
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{int(val)}\n({percentage:.1f}%)',
                       ha='center', va='bottom', fontsize=10, 
                       fontweight='bold', color='black')
    
    # Customize chart
    ax.set_xlabel('Disease Type', fontsize=14, fontweight='bold', color='black')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
    ax.set_title('Disease Type Distribution by Religion', 
                 fontsize=16, fontweight='bold', color='black', pad=20)
    ax.set_xticks(x + width * (len(religions) - 1) / 2)
    ax.set_xticklabels(cross_tab.index, rotation=45, ha='right', 
                       fontsize=11, color='black', fontweight='bold')
    ax.legend(title='Religion', fontsize=11, title_fontsize=12, 
              frameon=True, edgecolor='black')
    ax.tick_params(axis='y', labelsize=11, colors='black')
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add total valid responses text
    fig.text(0.99, 0.01, f'Total Valid Responses: {total_valid}', 
             ha='right', va='bottom', fontsize=11, 
             fontweight='bold', color='black',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig('disease_by_religion.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: disease_by_religion.png (Valid responses: {total_valid})")
    plt.close()

def create_disease_by_sex_chart(df):
    """Create bar chart for Disease Type Distribution by Sex"""
    # Remove rows with missing Disease or Sex data
    df_clean = df[df['Type_Of_Disease'].notna() & 
                  (df['Type_Of_Disease'] != '') & 
                  df['Sex'].notna() & 
                  (df['Sex'] != '')].copy()
    
    total_valid = len(df_clean)
    
    if total_valid == 0:
        print("No valid data for Disease Type by Sex")
        return
    
    # Create cross-tabulation
    cross_tab = pd.crosstab(df_clean['Type_Of_Disease'], df_clean['Sex'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set position of bars
    x = np.arange(len(cross_tab.index))
    width = 0.35
    
    # Plot bars for Male and Female
    if 'Male' in cross_tab.columns:
        male_values = cross_tab['Male'].values
        bars1 = ax.bar(x - width/2, male_values, width, 
                      label='Male', color='#3498DB',
                      edgecolor='black', linewidth=1.2)
        
        # Add labels
        for bar, val in zip(bars1, male_values):
            if val > 0:
                percentage = (val / total_valid) * 100
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{int(val)}\n({percentage:.1f}%)',
                       ha='center', va='bottom', fontsize=10, 
                       fontweight='bold', color='black')
    
    if 'Female' in cross_tab.columns:
        female_values = cross_tab['Female'].values
        bars2 = ax.bar(x + width/2, female_values, width, 
                      label='Female', color='#E74C3C',
                      edgecolor='black', linewidth=1.2)
        
        # Add labels
        for bar, val in zip(bars2, female_values):
            if val > 0:
                percentage = (val / total_valid) * 100
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{int(val)}\n({percentage:.1f}%)',
                       ha='center', va='bottom', fontsize=10, 
                       fontweight='bold', color='black')
    
    # Customize chart
    ax.set_xlabel('Disease Type', fontsize=14, fontweight='bold', color='black')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
    ax.set_title('Disease Type Distribution by Sex', 
                 fontsize=16, fontweight='bold', color='black', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(cross_tab.index, rotation=45, ha='right', 
                       fontsize=11, color='black', fontweight='bold')
    ax.legend(fontsize=12, frameon=True, edgecolor='black')
    ax.tick_params(axis='y', labelsize=11, colors='black')
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add total valid responses text
    fig.text(0.99, 0.01, f'Total Valid Responses: {total_valid}', 
             ha='right', va='bottom', fontsize=11, 
             fontweight='bold', color='black',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig('disease_by_sex.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: disease_by_sex.png (Valid responses: {total_valid})")
    plt.close()

def create_consanguinity_by_disease_chart(df):
    """Create bar chart for Consanguinity Distribution by Disease Type"""
    # Remove rows with missing Disease or Consanguinity data
    df_clean = df[df['Type_Of_Disease'].notna() & 
                  (df['Type_Of_Disease'] != '') & 
                  df['Consanguineous'].notna() & 
                  (df['Consanguineous'] != '')].copy()
    
    total_valid = len(df_clean)
    
    if total_valid == 0:
        print("No valid data for Consanguinity by Disease Type")
        return
    
    # Create cross-tabulation
    cross_tab = pd.crosstab(df_clean['Type_Of_Disease'], df_clean['Consanguineous'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set position of bars
    x = np.arange(len(cross_tab.index))
    width = 0.35
    
    # Plot bars for Yes and No
    if 'Yes' in cross_tab.columns:
        yes_values = cross_tab['Yes'].values
        bars1 = ax.bar(x - width/2, yes_values, width, 
                      label='Yes (Consanguineous)', color='#27AE60',
                      edgecolor='black', linewidth=1.2)
        
        # Add labels
        for bar, val in zip(bars1, yes_values):
            if val > 0:
                percentage = (val / total_valid) * 100
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{int(val)}\n({percentage:.1f}%)',
                       ha='center', va='bottom', fontsize=10, 
                       fontweight='bold', color='black')
    
    if 'No' in cross_tab.columns:
        no_values = cross_tab['No'].values
        bars2 = ax.bar(x + width/2, no_values, width, 
                      label='No (Non-Consanguineous)', color='#E67E22',
                      edgecolor='black', linewidth=1.2)
        
        # Add labels
        for bar, val in zip(bars2, no_values):
            if val > 0:
                percentage = (val / total_valid) * 100
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                       f'{int(val)}\n({percentage:.1f}%)',
                       ha='center', va='bottom', fontsize=10, 
                       fontweight='bold', color='black')
    
    # Customize chart
    ax.set_xlabel('Disease Type', fontsize=14, fontweight='bold', color='black')
    ax.set_ylabel('Count', fontsize=14, fontweight='bold', color='black')
    ax.set_title('Consanguinity Distribution by Disease Type', 
                 fontsize=16, fontweight='bold', color='black', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(cross_tab.index, rotation=45, ha='right', 
                       fontsize=11, color='black', fontweight='bold')
    ax.legend(fontsize=11, frameon=True, edgecolor='black')
    ax.tick_params(axis='y', labelsize=11, colors='black')
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add total valid responses text
    fig.text(0.99, 0.01, f'Total Valid Responses: {total_valid}', 
             ha='right', va='bottom', fontsize=11, 
             fontweight='bold', color='black',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig('consanguinity_by_disease.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: consanguinity_by_disease.png (Valid responses: {total_valid})")
    plt.close()

def main():
    """Main function to generate all charts"""
    print("=" * 60)
    print("GENERATING BAR GRAPHS FROM DATA.CSV")
    print("=" * 60)
    
    # Load data
    df = load_and_clean_data('DATA.csv')
    
    if df is None:
        print("Failed to load data. Exiting.")
        return
    
    print(f"\nTotal rows in dataset: {len(df)}")
    print("\nGenerating charts...\n")
    
    # Generate all three charts
    try:
        create_disease_by_religion_chart(df)
    except Exception as e:
        print(f"✗ Error creating disease by religion chart: {e}")
    
    try:
        create_disease_by_sex_chart(df)
    except Exception as e:
        print(f"✗ Error creating disease by sex chart: {e}")
    
    try:
        create_consanguinity_by_disease_chart(df)
    except Exception as e:
        print(f"✗ Error creating consanguinity by disease chart: {e}")
    
    print("\n" + "=" * 60)
    print("COMPLETED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
