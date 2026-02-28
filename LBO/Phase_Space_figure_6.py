"""
this file is to simulate the 6th figure
the graph describes the phase space dynamics of LBO
The fig includes:

Phase Space plots (Amplitude vs delayed Amplitude)
for three different equivalence ratios.

We find:
Stable (0.769) --> tight, small attractor at the center
Transition (0.865) --> attractor begins to spread
Near LBO (1.065) --> large, chaotic 'cloud' with no clear 
periodicity, showing the onset of blowout precursors.
"""

"""
Prof De wants a phase space for LBO like we did for TAI.
I am using a time delay (tau) to create the 2D plot.
For LBO, we don't expect a circle (limit cycle), but 
a chaotic attractor that shows the instability.
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

# using the same indices for the story: 90, 80, and 65 SLPM
plot_indices = [9, 3, 0]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, idx in enumerate(plot_indices):
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    # open the file
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # signal processing
    signal = df1['Amplitude'].to_numpy()
    signal = signal - np.mean(signal) # centering
    
    # define a time delay (tau) 
    # for 44100Hz, a delay of 10-20 samples works well
    tau = 15 
    
    # plot the phase space (x(t) vs x(t + tau))
    axes[i].plot(signal[:-tau], signal[tau:], color='black', linewidth=0.5, alpha=0.6)
    
    axes[i].set_title(f"Φ = {phi_value:.3f}")
    axes[i].set_xlabel("x(t)")
    axes[i].set_ylabel("x(t + τ)")
    axes[i].grid(True, alpha=0.2)

plt.suptitle("Figure 6: Phase Space Dynamics Approaching LBO")
plt.tight_layout()
plt.savefig("Figure_6_LBO_PhaseSpace.png", dpi=300)
plt.show()