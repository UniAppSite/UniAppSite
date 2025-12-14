import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('DataF.csv')

# Define question labels for better readability
questions = {
    'Q1': '1. Would you consider getting genetic counseling before planning\na marriage or a pregnancy in the future?',
    'Q2': '2. How often in your family are the genetic risks of consanguineous\nmarriages of the future child addressed before the marriage?',
    'Q3': '3. How often are screening camps for hemoglobinopathies\ndone in your locality?',
    'Q4': '4. How interested would you be to participate if a free\nscreening camp is conducted nearby?'
}

# Define response labels (adjust based on your scale)
response_labels = {
    1: 'Response 1',
    2: 'Response 2',
    3: 'Response 3'
}

# Column names from CSV
columns = df.columns.tolist()

# Create 4 separate bar graphs
for idx, col in enumerate(columns, 1):
    # Remove missing values and count responses
    data = df[col].dropna()
    value_counts = data.value_counts().sort_index()
    
    # Calculate total valid responses
    total = len(data)
    
    # Calculate percentages
    percentages = (value_counts / total * 100).round(1)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    x_pos = np.arange(len(value_counts))
    bars = ax.bar(x_pos, value_counts.values, color=['#4472C4', '#ED7D31', '#A5A5A5'][:len(value_counts)], 
                   edgecolor='black', linewidth=1.2, alpha=0.85)
    
    # Customize the plot
    ax.set_xlabel('Response Options', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Respondents', fontsize=12, fontweight='bold')
    ax.set_title(f'Question {idx}\n{questions[f"Q{idx}"]}', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([response_labels.get(int(val), f'Option {int(val)}') 
                        for val in value_counts.index], fontsize=11)
    
    # Add value labels on bars (count and percentage)
    for i, (bar, count, pct) in enumerate(zip(bars, value_counts.values, percentages.values)):
        height = bar.get_height()
        # Add count
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(count)}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
        # Add percentage
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'{pct}%',
                ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Add grid for better readability
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    
    # Add total respondents information
    ax.text(0.98, 0.98, f'Total Valid Responses: {total}',
            transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(f'question_{idx}_analysis.png', dpi=300, bbox_inches='tight')
    print(f'Saved: question_{idx}_analysis.png')
    
    # Close the figure to free memory
    plt.close()

print('\n=== Analysis Complete ===')
print(f'Total respondents in dataset: {len(df)}')
print('\nSummary for each question:')
for idx, col in enumerate(columns, 1):
    data = df[col].dropna()
    print(f'\nQuestion {idx}:')
    print(f'  Valid responses: {len(data)}')
    print(f'  Missing responses: {df[col].isna().sum()}')
    value_counts = data.value_counts().sort_index()
    for val, count in value_counts.items():
        pct = (count / len(data) * 100)
        print(f'  Option {int(val)}: {int(count)} ({pct:.1f}%)')
