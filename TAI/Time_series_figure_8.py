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
folder_path = "TAI" 
re_map = {15: 1565.85, 40: 4175.60, 53: 5532.67}
plot_files = [15, 40, 53]

# sampling frequency of the DAQ
fs = 44100

# sharey=True to show amplitude growth clearly
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, sharey=True)

for i, file_num in enumerate(plot_files):

    re_val = re_map[file_num]

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")

    # read amplitude column
    df = pd.read_excel(file_name, header=None)

    signal = df[0].to_numpy()

    # subtract mean to center the signal
    signal = signal - np.mean(signal)

    # create time axis
    time = np.arange(len(signal)) / fs

    # select first 10 seconds
    mask = time <= 10

    axes[i].plot(time[mask], signal[mask], linewidth=0.4)

    axes[i].set_ylabel("Fluctuation (V)")
    axes[i].set_title(f"Re = {re_val:.2f}")

    axes[i].grid(True, alpha=0.3)

plt.xlabel("Time (s)")

plt.tight_layout()

plt.savefig("Figure_8_TAI_TimeSeries.png", dpi=300)

plt.show()