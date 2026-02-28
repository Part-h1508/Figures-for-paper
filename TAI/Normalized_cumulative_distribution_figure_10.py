"""
this file is to simulate the 10th figure
the graph describes the TAI precursor duration (Theta)
The fig includes:

Normalized cumulative duration (Theta) vs Reynolds Number.
Uses the 3-sigma threshold method.

We find:
threshold = 3 * std(stable_signal)
--> theta is ~0 for stable conditions
--> theta increases as Re increases
--> shows the transition to full instability
"""

"""
Prof De wants the 3-sigma method for TAI.
I am using the first file (15.xlsx) as the 'stable' baseline 
to calculate the threshold. Then I apply that threshold 
to all other files to see how many points exceed it.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# variables
folder_path = "TAI" 
# Reynolds mapping for the X-axis
re_data = {
    15: 1565.85, 20: 2087.80, 25: 2609.75, 30: 3131.70, 
    35: 3653.65, 40: 4175.60, 45: 4697.55, 50: 5219.50, 53: 5532.67
}
fs = 44100

# 1. Calculate the 3-sigma threshold from the STABLE case (Re 1565)
stable_file = os.path.join(folder_path, "15.xlsx")
df_stable = pd.read_excel(stable_file, header=None)
stable_signal = df_stable[0].to_numpy()
stable_signal = stable_signal - np.mean(stable_signal)
threshold = 3 * np.std(stable_signal)

theta_values = []
re_list = []

# 2. Calculate Theta for all files
for file_num, re_val in sorted(re_data.items()):
    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    df = pd.read_excel(file_name, header=None)
    
    signal = df[0].to_numpy()
    signal = signal - np.mean(signal) # center signal
    
    # count points exceeding the 3rd standard deviation of noise
    count_exceed = np.sum(np.abs(signal) > threshold)
    theta = count_exceed / len(signal)
    
    theta_values.append(theta)
    re_list.append(re_val)

# 3. Plotting
plt.figure(figsize=(8, 6))
plt.plot(re_list, theta_values, marker='o', linestyle='-', color='blue')

plt.xlabel("Reynolds Number (Re)")
plt.ylabel("Normalized Cumulative Duration (Θ)")
plt.title("Figure 10: TAI Precursor Duration")
plt.grid(True, alpha=0.3)

# saving for the repo
plt.savefig("Figure_10_TAI_Theta.png", dpi=300)
plt.show()