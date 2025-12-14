import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('EsectionData.csv')

# Print basic information about the data
print(f"Total respondents: {len(df)}")
print(f"\nColumn names:")
for i, col in enumerate(df.columns, 1):
    print(f"Q{i}: {col}")

# Question labels (shortened for better display)
questions = [
    "Q1: Consanguineous marriages\nshould be avoided",
    "Q2: Genetic testing before marriage\nshould be mandatory",
    "Q3: Would advise friends/relatives\nagainst consanguineous marriage",
    "Q4: Acceptable to get tested\nfor genetic diseases",
    "Q5: General preference towards\nconsanguineous marriage"
]

# Create 5 separate bar graphs
for i, col in enumerate(df.columns):
    # Count the frequency of each response (1-5 scale)
    # Remove NaN values before counting
    response_counts = df[col].dropna().value_counts().sort_index()
    
    # Create figure with larger size for better readability
    plt.figure(figsize=(10, 6))
    
    # Create bar chart
    bars = plt.bar(response_counts.index, response_counts.values, 
                   color='steelblue', edgecolor='black', linewidth=1.2)
    
    # Add value labels on top of each bar with count and percentage
    total_responses = df[col].notna().sum()
    for bar in bars:
        height = bar.get_height()
        percentage = (height / total_responses) * 100
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}\n({percentage:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Customize the plot
    plt.xlabel('Response Scale (1=Strongly Disagree, 5=Strongly Agree)', 
              fontsize=12, fontweight='bold', labelpad=10)
    plt.ylabel('Number of Respondents', fontsize=12, fontweight='bold', labelpad=10)
    plt.title(f'{questions[i]}\n(n={df[col].notna().sum()} respondents)', 
             fontsize=13, fontweight='bold', pad=20)
    
    # Set x-axis to show all possible responses (1-5)
    plt.xticks([1, 2, 3, 4, 5], fontsize=11)
    plt.yticks(fontsize=11)
    
    # Add grid for better readability
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adjust layout to prevent text collision
    plt.tight_layout()
    
    # Save the figure
    filename = f'question_{i+1}_analysis.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {filename}")
    
    # Display statistics for this question
    print(f"\nQuestion {i+1} Statistics:")
    print(f"Valid responses: {df[col].notna().sum()}")
    print(f"Mean: {df[col].mean():.2f}")
    print(f"Median: {df[col].median():.2f}")
    print(f"Mode: {df[col].mode().values[0] if len(df[col].mode()) > 0 else 'N/A'}")
    print(f"Response distribution:")
    for value, count in response_counts.items():
        percentage = (count / df[col].notna().sum()) * 100
        print(f"  {int(value)}: {int(count)} ({percentage:.1f}%)")
    
    # Close the figure to free memory
    plt.close()

print("\n" + "="*50)
print("All graphs have been created successfully!")
print("="*50)
