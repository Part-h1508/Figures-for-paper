"""
this file is to simulate the 12th figure
the graph describes the persistence of the TAI rhythm
The fig includes:

Autocorrelation curves for three Reynolds numbers.

We find:
Stable (Re: 1565.85) --> Sharp decay to zero (random noise)
Intermittent (Re: 4175.60) --> Oscillations with decaying envelope
Limit Cycle (Re: 5532.67) --> Persistent, steady sine-wave 
    (deterministic memory of the limit cycle)
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
fs = 44100  # High resolution sampling frequency

plt.figure(figsize=(10, 6))

for file_num in plot_files:
    re_val = re_map[file_num]
    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    # Read amplitude from single column
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()
    
    # Center the signal
    signal = signal - np.mean(signal)
    
    # We look at 40ms of lag to see multiple cycles
    max_lag = int(0.04 * fs) 
    
    # Calculating autocorrelation using FFT (faster for large signals)
    # We normalize such that Rxx(0) = 1.0
    fft = np.fft.fft(np.concatenate([signal, np.zeros(len(signal))]))
    corr = np.fft.ifft(fft * np.conj(fft)).real[:max_lag]
    corr = corr / corr[0]
    
    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag_time_ms, corr, label=f"Re = {re_val:.2f}")

# Formatting for the paper
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")
plt.title("Figure 12: TAI Autocorrelation Persistence")
plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Reynolds Number (Re)")
plt.tight_layout()

# Saving for the repo
plt.savefig("Figure_12_TAI_Autocorrelation.png", dpi=300)
plt.show()