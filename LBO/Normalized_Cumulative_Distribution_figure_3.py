"""
this file is to simulate the 3rd figure
the graph describes physical behaviour of the line
The fig includes:

Normalized cumulative duration of LBO precursor events at
different working conditions.

We find:
mean voltage --> blowout threshold at 72%
--> count data points below threshold
--> divide the count by total data points
"""

"""
Prof De reminded me that the LBO threshold should be 72%.
I am using the 'Fi/FI_LBO' column for the X-axis because
it shows the transition reaching the limit at 1.0.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14
})

folder_path = "."
main_file = os.path.join(folder_path, "Data details.xlsx")

df = pd.read_excel(main_file)

x_axis_col = "Fi/FI_LBO"
threshold = 0.72

theta_values = []
for idx, row in df.iterrows():
    air_value = row["Air (SLPM)"]
    file_name = os.path.join(folder_path, f"{int(air_value)}.xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])
    
    count_below = (df1['Amplitude'] < threshold).sum()
    total = len(df1)
    theta = count_below / total
    theta_values.append(theta)

plt.figure(figsize=(8, 6))

plt.plot(df[x_axis_col], theta_values, marker='o', markersize=6, linewidth=2)

plt.axhline(y=0.02, linestyle='--', linewidth=1.5)

plt.xlabel("Φ / Φ_LBO", fontsize=18)
plt.ylabel("Θ", fontsize=18)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Figure_3_LBO_Theta_revised.png", dpi=300)
plt.show()