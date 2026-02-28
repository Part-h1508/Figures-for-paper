"""
this file is to simulate the 1st figure
the graph describes physical behaviour of the raw signals
The fig includes:

Three subplots showing the time series evolution:
1. Lowest Equivalence ratio (0.769) -> Far from LBO
2. Middle Equivalence ratio (0.865) -> Approaching LBO
3. Highest Equivalence ratio (1.065) -> Near/At LBO

We find:
raw signal --> steady oscillations at low Phi
--> increased irregularity at middle Phi
--> distinct intermittency/dips at highest Phi
"""

"""
I am using the 'Equivalence ratio' column for the physics.
Based on the datasheet, 90 SLPM is our most stable point (0.769)
and 65 SLPM is our blowout point (1.065).
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
phi_name = "Equivalence ratio"

# open the main data file
df = pd.read_excel(main_file)

# select the indices for lowest, middle, and highest Phi
# index 9 (90 SLPM) --> 0.768
# index 3 (80 SLPM) --> 0.865
# index 0 (65 SLPM) --> 1.064
plot_indices = [9, 3, 0] 

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

for i, idx in enumerate(plot_indices):
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    # open the file from the LBO folder
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # calculate sampling frequency from the data
    delta_t = df1['Time'].iloc[1] - df1['Time'].iloc[0]
    fs = 1 / delta_t
    
    # time axis in ms starting from zero
    time_ms = (df1['Time'] - df1['Time'].iloc[0]) * 1000

    # plot 100ms window to show individual oscillations
    num_samples = int(0.1 * fs)
    axes[i].plot(time_ms[:num_samples], df1['Amplitude'][:num_samples], color='red', linewidth=0.8)
    
    # labeling with Equivalence ratio per Prof De's request
    axes[i].set_title(f"Equivalence Ratio (Φ): {phi_value:.3f}")
    axes[i].set_ylabel("Amplitude")
    axes[i].grid(True, alpha=0.3)

plt.xlabel("Time (ms)")
plt.suptitle("Figure 1: Time Series Evolution approaching LBO", fontsize=14)
plt.tight_layout()
plt.show()