"""
this file is to simulate the 8th figure
the graph describes physical behaviour of the TAI transition
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

# sampling frequency of your DAQ
fs = 44100

# added sharey=True to make the amplitude growth visible
fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True, sharey=True)

for i, file_num in enumerate(plot_files):

    re_val = re_map[file_num]
    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    # read amplitude only (handling the single column format)
    df = pd.read_excel(file_name, header=None)
    
    # using the first column for amplitude
    signal = df[0].to_numpy()

    # subtract mean (center signal) to show fluctuations
    signal = signal - np.mean(signal)

    # generate time axis manually based on sampling frequency
    time = np.arange(len(signal)) / fs
    time_ms = time * 1000

    # select first 50 ms to show the sine waves clearly
    mask = time_ms <= 50

    axes[i].plot(
        time_ms[mask],
        signal[mask],
        color='blue',
        linewidth=0.8
    )

    axes[i].set_title(f"Reynolds Number (Re): {re_val:.2f}")
    axes[i].set_ylabel("Fluctuation (V)")
    axes[i].grid(True, alpha=0.3)

plt.xlabel("Time (ms)")
plt.suptitle("Figure 8: TAI Evolution (Unified Scale)", fontsize=14)
plt.tight_layout()

plt.savefig("Figure_8_TAI_TimeSeries_Unified.png", dpi=300)
plt.show()