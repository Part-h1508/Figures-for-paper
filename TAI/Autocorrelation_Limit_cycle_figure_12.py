"""
this file is to simulate autocorrelation for TAI (original method)
the graph describes temporal behaviour of pressure signal

we use FFT-based autocorrelation (faster than np.correlate)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import signal

# variables
folder_path = "TAI"

# mapping files to Reynolds number
re_map = {
    15: 1565.85,  
    40: 4175.60, 
    53: 5532.67
}

plt.figure(figsize=(10, 6))

# Define line styles
linestyles = ['-', '--', ':']
fs = 44100
samples_needed = int(2 * fs)  # 2 seconds
max_lag = int(0.02 * fs)  # 20 ms

for idx, (file_num, re_val) in enumerate(re_map.items()):

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    # Read only the first 2 seconds of data
    df = pd.read_excel(file_name, header=None, nrows=samples_needed)
    signal_data = df[0].to_numpy()

    # remove mean
    signal_data = signal_data - np.mean(signal_data)

    # autocorrelation using FFT (much faster than np.correlate)
    corr = signal.correlate(signal_data, signal_data, mode='same', method='fft')
    center = len(corr) // 2

    # normalize by peak (at lag 0)
    corr = corr / corr[center]

    # extract only the lag window we need (20 ms)
    rxx = corr[center:center + max_lag]

    lag = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag, rxx, linestyle=linestyles[idx], linewidth=2, label=f"Re = {re_val:.0f}")

plt.xlabel("Lag Time (ms)", fontsize=20)
plt.ylabel("Autocorrelation Function", fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.grid(True, alpha=0.3)
plt.legend(fontsize=20)

plt.tight_layout()
plt.savefig("Figure_TAI_Autocorrelation_original_1.png", dpi=300)
plt.show()