"""
this file is to simulate the 6th figure
the graph describes the phase space dynamics of LBO.

The attractor structure is shown for three operating conditions:
1. Stable flame
2. Transition regime
3. Near blowout condition
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

# selecting the three cases used earlier in the analysis
# index 0 -> 65 SLPM (highest Φ)
# index 3 -> 80 SLPM
# index 9 -> 90 SLPM (lowest Φ)
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

    # remove mean so the attractor is centered
    signal = signal - np.mean(signal)

    # time delay
    tau = 15

    # phase space plot
    axes[i].plot(signal[:-tau], signal[tau:], color='black', linewidth=0.4, alpha=0.4)

    # labeling with equivalence ratio
    axes[i].set_title(f"Φ = {phi_value:.3f}")

    axes[i].set_xlabel("x(t)")
    axes[i].set_ylabel("x(t + τ)")

    axes[i].grid(True, alpha=0.2)

    # fixed axis limits to compare attractor growth
    axes[i].set_xlim(-2.5, 2.5)
    axes[i].set_ylim(-2.5, 2.5)

plt.tight_layout()

plt.savefig("Figure_6_LBO_PhaseSpace.png", dpi=300)

plt.show()