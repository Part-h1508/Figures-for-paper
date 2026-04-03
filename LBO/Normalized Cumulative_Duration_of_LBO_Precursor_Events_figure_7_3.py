"""
this file is to simulate figure 7.3
the graph describes the total time spent in blowout state
The fig includes:

Theta values (Normalized Cumulative Duration) vs Phi/Phi_lbo.
This follows the exact logic of Fig. 9 in the Yi and Gutmark paper.

We find:
threshold = 0.72 * mean
--> theta stays at zero during stable operation (Fi/FI_LBO < 1.0)
--> theta spikes sharply as the limit approaches 1.0
--> this represents the 'cumulative duration' of flame flickers
"""

"""
Prof De wants me to show that the precursors are measurable.
By using the 72% threshold, we are catching the 'dips' in 
the green PDF we saw in Fig 7.2. I am plotting theta 
against the normalized ratio to show the blowout limit.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
x_axis_col = "Fi/FI_LBO" # standard for comparing LBO across different airflows

# open the main data file
df = pd.read_excel(main_file)

# list to store theta
theta_values = []

# loop thru to calculate Theta for each condition
for index, row in df.iterrows():
    air_value = row[air_name]
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # calculate mean and threshold
    mean_amp = df1['Amplitude'].mean()
    threshold = 0.72 * mean_amp
    
    # count points below threshold (precursor duration)
    count_precursors = (df1['Amplitude'] < threshold).sum()
    theta = count_precursors / len(df1['Amplitude'])
    
    theta_values.append(theta)

# plot the Theta curve
plt.figure(figsize=(8, 6))
plt.plot(df[x_axis_col], theta_values, marker='^', color='tab:red', label='Precursor Duration (Θ)')

# draw threshold lines
plt.axvline(x=1.0592, linestyle='--', color='black', linewidth=1.5)
plt.axhline(y=0.0251, linestyle='--', color='black', linewidth=1.5)

# add text at intersection point
plt.text(1.065, 0.035, 'threshold = 1.0592', fontsize=12, verticalalignment='bottom', horizontalalignment='left')

plt.xlabel("$\\Phi/\\Phi_{{LBO}}$", fontsize=22)
plt.ylabel('Θ', fontsize=22)

plt.tick_params(axis='both', which='major', labelsize=20)

plt.grid(True, alpha=0.3)
plt.savefig("Figure_7_3_LBO_Theta_Final_fonted.png", dpi=300)
plt.show()