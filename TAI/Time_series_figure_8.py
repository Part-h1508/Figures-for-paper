"""
this file is to simulate the 8th figure
the graph describes physical behaviour of the TAI transition

Prof mentioned we should show the full time series window
from 0 to 10 seconds so that the transition from stable to
limit cycle behaviour is clearly visible.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# variables
folder_path = "."
re_map = {15: 1565.85, 40: 4175.60, 53: 5532.67}
plot_files = [15, 40, 53]
fs = 44100

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "axes.titlesize": 18
})

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, sharey=True)

for i, file_num in enumerate(plot_files):
    re_val = re_map[file_num]

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    df = pd.read_excel(file_name, header=None)

    signal = df[0].to_numpy()
    signal = signal.copy()
    signal -= np.mean(signal)

    time = np.arange(len(signal)) / fs
    mask = time <= 10

    axes[i].plot(time[mask], signal[mask], linewidth=0.7)

    axes[i].set_title(f"Re = {re_val:.2f}", fontsize=18)
    axes[i].set_ylabel("Fluctuation (V)", fontsize=16)
    axes[i].grid(True, alpha=0.3)

axes[-1].set_xlabel("Time (s)", fontsize=18)

plt.tight_layout()
plt.savefig("Figure_8_TAI_TimeSeries.png", dpi=300)
plt.show()