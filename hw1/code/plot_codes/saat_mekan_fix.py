#Can Günyel 150200049
import re
import matplotlib.pyplot as plt
import numpy as np

# Open the file (file names change each time)
file_path = "aksam/norway_aksam.txt"
with open(file_path, 'r') as file:
    file_contents = file.read()

tek = file_contents.split("\n")
tek = [item for item in tek if item.strip() != ""]

# Initialize an dictionary
website_data = {
    "24/10/23": [],
    "25/10/23": [],
    "26/10/23": [],
    
}




values = []
for line in tek:
    if line.startswith("Results for"):
        website_name = line.split("Results for ")[1].split(" (Ping Count")[0]#varying parameter
    else:
        values = line.split(",")
        for x in values:#extracting values
            website_data[website_name].append(int(x))

# Calculate the minimum, maximum, and average 
website_min_values = {website: min(times) for website, times in website_data.items()}
website_max_values = {website: max(times) for website, times in website_data.items()}
website_avg_values = {website: round(sum(times) / len(times), 1) for website, times in website_data.items()}

# Extract x axis
websites = list(website_min_values.keys())


bar_width = 0.25
index = np.arange(len(websites))

# plotting max,min,avg
plt.bar(index, list(website_min_values.values()), bar_width, label="Minimum")
plt.bar(index + bar_width, list(website_max_values.values()), bar_width, label="Maximum")
plt.bar(index + 2 * bar_width, list(website_avg_values.values()), bar_width, label="Average")

# Add numerical values to the bars
fontsize = 8
for i, min_value in enumerate(website_min_values.values()):
    plt.text(index[i] - 0.08, min_value + 1, "{:.1f}".format(min_value), ha='center', va='bottom', fontsize=fontsize)
for i, max_value in enumerate(website_max_values.values()):
    plt.text(index[i] + bar_width, max_value + 1, "{:.1f}".format(max_value), ha='center', va='bottom', fontsize=fontsize)
for i, avg_value in enumerate(website_avg_values.values()):
    plt.text(index[i] + 2 * bar_width, avg_value + 1, "{:.1f}".format(avg_value), ha='center', va='bottom', fontsize=fontsize)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Time (milliseconds)')
plt.title('Website Loading Times (Minimum, Maximum, and Average)')


plt.xticks(index + bar_width, websites, rotation=80)

plt.legend()
plt.tight_layout()
plt.show()
