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

Prof mentioned we should plot the FULL time series (20 seconds)
instead of the earlier 100 ms window so the intermittency can be seen clearly.
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

plot_indices = [9, 3, 0]

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

for i, idx in enumerate(plot_indices):
    row = df.iloc[idx]
    air_value = row["Air (SLPM)"]
    phi_value = row["Equivalence ratio"]

    file_name = os.path.join(folder_path, f"{int(air_value)}.xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    time_s = df1['Time'] - df1['Time'].iloc[0]

    axes[i].plot(time_s, df1['Amplitude'], linewidth=0.7)

    axes[i].set_title(f"Φ = {phi_value:.3f}", fontsize=18)
    axes[i].set_ylabel("Amplitude", fontsize=16)
    axes[i].grid(True, alpha=0.3)

axes[-1].set_xlabel("Time (s)", fontsize=18)

plt.tight_layout()
plt.savefig("Figure_1_TimeSeriesLBO_fonted.png", dpi=300)
plt.show()