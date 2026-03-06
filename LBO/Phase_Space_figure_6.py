"""
this file is to simulate the 6th figure
the graph describes the phase space dynamics of LBO.
Following Prof. De's instructions, we focus on the lowest 
equivalence ratio (Phi) as the blowout point.
"""

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

# Plot indices updated to match the physical story:
# 65 SLPM (Stable/Highest Phi) -> 80 SLPM (Transition) -> 90 SLPM (Blowout/Lowest Phi)
plot_indices = [0, 3, 9]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, idx in enumerate(plot_indices):
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # signal processing
    signal = df1['Amplitude'].to_numpy()
    signal = signal - np.mean(signal) # centering for attractor focus
    
    # Time delay (tau). For LBO, 15-20 samples (approx 0.4ms) captures 
    # the stochastic spread well.
    tau = 15 
    
    # plot the phase space (x(t) vs x(t + tau))
    axes[i].plot(signal[:-tau], signal[tau:], color='black', linewidth=0.5, alpha=0.4)
    
    # Dynamic title based on the state
    state = "Stable" if air_value == 65 else "Transition" if air_value == 80 else "Lowest Phi (LBO)"
    axes[i].set_title(f"{state}\nΦ = {phi_value:.3f}")
    
    axes[i].set_xlabel("x(t)")
    axes[i].set_ylabel("x(t + τ)")
    axes[i].grid(True, alpha=0.2)
    
    # Consistent axis limits help visualize the growth of the attractor
    axes[i].set_xlim(-2.5, 2.5)
    axes[i].set_ylim(-2.5, 2.5)

plt.suptitle("Figure 6: Phase Space Dynamics Approaching LBO (Corrected Mapping)")
plt.tight_layout()
plt.savefig("Figure_6_LBO_PhaseSpace_Final.png", dpi=300)
plt.show()