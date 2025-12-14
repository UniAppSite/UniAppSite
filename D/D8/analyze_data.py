import csv
import matplotlib.pyplot as plt

# Read the CSV file
csv_file = 'Data.csv'
responses = []

with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for i, row in enumerate(csv_reader):
        if i == 0:  # Skip header
            continue
        if row and row[0].strip():  # Skip empty rows
            responses.append(row[0].strip())

# Count options based on comma count
# 1 comma = 2 options
# 0 commas = 1 option
# 2 commas = 3 options, etc.

one_option = 0
two_options = 0
three_options = 0
four_options = 0
five_or_more = 0

two_option_responses = []

for response in responses:
    comma_count = response.count(',')
    
    if comma_count == 0:
        one_option += 1
    elif comma_count == 1:
        two_options += 1
        two_option_responses.append(response)
    elif comma_count == 2:
        three_options += 1
    elif comma_count == 3:
        four_options += 1
    else:
        five_or_more += 1

# Calculate total and percentages
total = len(responses)
two_option_percentage = (two_options / total) * 100 if total > 0 else 0
other_percentage = 100 - two_option_percentage

# Create text report
report_filename = 'analysis_report.txt'
with open(report_filename, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("CSV DATA ANALYSIS REPORT - TWO OPTION SELECTIONS\n")
    f.write("="*70 + "\n\n")
    
    f.write(f"Total Responses: {total}\n\n")
    
    f.write("-"*70 + "\n")
    f.write("BREAKDOWN BY NUMBER OF OPTIONS SELECTED:\n")
    f.write("-"*70 + "\n")
    f.write(f"1 Option:       {one_option:3d} responses ({one_option/total*100:.2f}%)\n")
    f.write(f"2 Options:      {two_options:3d} responses ({two_option_percentage:.2f}%)\n")
    f.write(f"3 Options:      {three_options:3d} responses ({three_options/total*100:.2f}%)\n")
    f.write(f"4 Options:      {four_options:3d} responses ({four_options/total*100:.2f}%)\n")
    f.write(f"5+ Options:     {five_or_more:3d} responses ({five_or_more/total*100:.2f}%)\n\n")
    
    f.write("="*70 + "\n")
    f.write("KEY FINDING: TWO-OPTION SELECTIONS\n")
    f.write("="*70 + "\n")
    f.write(f"Count:      {two_options} people selected exactly 2 options\n")
    f.write(f"Percentage: {two_option_percentage:.2f}% of all responses\n\n")
    
    f.write("-"*70 + "\n")
    f.write("ALL TWO-OPTION RESPONSES:\n")
    f.write("-"*70 + "\n")
    for i, resp in enumerate(two_option_responses, 1):
        f.write(f"{i:3d}. {resp}\n")

print(f"Report saved to: {report_filename}")
print(f"\nSummary:")
print(f"Total responses: {total}")
print(f"People who selected exactly 2 options: {two_options} ({two_option_percentage:.2f}%)")

# Create pie chart
labels = ['Selected 2 Options', 'Other (1, 3+ Options)']
sizes = [two_options, total - two_options]
colors = ['#ff9999', '#66b3ff']
explode = (0.1, 0)  # Explode the first slice

plt.figure(figsize=(10, 8))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90, textprops={'fontsize': 12})
plt.title('Distribution of Responses: Two-Option Selections vs Others', 
          fontsize=14, fontweight='bold', pad=20)

# Add count information
plt.text(0, -1.3, f'Total Responses: {total}', ha='center', fontsize=11)
plt.text(0, -1.45, f'2 Options: {two_options} | Other: {total - two_options}', 
         ha='center', fontsize=10)

plt.axis('equal')
plt.tight_layout()
plt.savefig('two_options_piechart.png', dpi=300, bbox_inches='tight')
print(f"Pie chart saved to: two_options_piechart.png")

plt.show()
