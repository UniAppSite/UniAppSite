import pandas as pd
import matplotlib.pyplot as plt
import os

# Read the CSV file with proper encoding handling
try:
    df = pd.read_csv('DQ1.csv', encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv('DQ1.csv', encoding='latin-1')
    except UnicodeDecodeError:
        df = pd.read_csv('DQ1.csv', encoding='cp1252')

# Create output directory for charts
output_dir = 'pie_charts'
os.makedirs(output_dir, exist_ok=True)

# Define colors for consistent visualization
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6']

# Get all column names (questions)
questions = df.columns.tolist()

# Create a pie chart for questions 1-7, bar chart for question 8
for i, question in enumerate(questions, 1):
    # Count the values for this question
    value_counts = df[question].value_counts()
    
    # Determine if this should be a bar chart (last question/question 8) or pie chart
    is_bar_chart = (i == len(questions))
    
    if is_bar_chart:
        # Create bar chart for question 8
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Create bar chart
        bars = ax.bar(range(len(value_counts)), value_counts.values, color=colors[:len(value_counts)])
        
        # Add value labels on top of bars with count and percentage
        total = value_counts.sum()
        for idx, (bar, count) in enumerate(zip(bars, value_counts.values)):
            percentage = (count / total) * 100
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}\n({percentage:.1f}%)',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Set x-axis labels
        ax.set_xticks(range(len(value_counts)))
        ax.set_xticklabels(value_counts.index, rotation=45, ha='right', fontsize=10)
        
        # Set labels and title
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax.set_xlabel('Response', fontsize=12, fontweight='bold')
        title = question if len(question) <= 80 else question[:77] + '...'
        ax.set_title(f'Question {i}: {title}', fontsize=12, fontweight='bold', wrap=True, pad=20)
        
        # Add grid for better readability
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save the figure
        filename = f'{output_dir}/question_{i}_barchart.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f'Saved: {filename}')
        
        # Close the figure to free memory
        plt.close()
    else:
        # Create pie chart for questions 1-7
        num_segments = len(value_counts)
        fig_size = (12, 10) if num_segments > 5 else (10, 8)
        fig, ax = plt.subplots(figsize=fig_size)
        
        # Create labels with both count and percentage
        labels = []
        for label, count in value_counts.items():
            percentage = (count / value_counts.sum()) * 100
            labels.append(f'{label}\n({count}, {percentage:.1f}%)')
        
        # For charts with many segments, use legend instead of direct labels
        if num_segments > 6:
            # Create the pie chart without labels on the chart
            wedges, texts, autotexts = ax.pie(
                value_counts.values,
                labels=None,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(value_counts)],
                textprops={'fontsize': 9},
                pctdistance=0.85
            )
            
            # Create legend with labels
            legend_labels = []
            for label, count in value_counts.items():
                percentage = (count / value_counts.sum()) * 100
                legend_labels.append(f'{label}: {count} ({percentage:.1f}%)')
            
            ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
        else:
            # Create the pie chart with labels for fewer segments
            wedges, texts, autotexts = ax.pie(
                value_counts.values,
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(value_counts)],
                textprops={'fontsize': 9},
                pctdistance=0.85,
                labeldistance=1.1
            )
        
        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # Set title (truncate if too long)
        title = question if len(question) <= 80 else question[:77] + '...'
        ax.set_title(f'Question {i}: {title}', fontsize=12, fontweight='bold', wrap=True, pad=20)
        
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the figure
        filename = f'{output_dir}/question_{i}_piechart.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f'Saved: {filename}')
        
        # Close the figure to free memory
        plt.close()

print(f'\nAll pie charts have been created and saved in the "{output_dir}" directory!')

# Print summary statistics
print('\n' + '='*60)
print('SUMMARY OF RESPONSES')
print('='*60)
for i, question in enumerate(questions, 1):
    print(f'\nQuestion {i}: {question}')
    print('-' * 60)
    value_counts = df[question].value_counts()
    total = value_counts.sum()
    for label, count in value_counts.items():
        percentage = (count / total) * 100
        print(f'  {label}: {count} ({percentage:.1f}%)')
