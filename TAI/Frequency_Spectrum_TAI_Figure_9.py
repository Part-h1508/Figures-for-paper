"""
this file is to simulate the 9th figure
the graph describes the frequency peaks of TAI
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch
import numpy as np
import os

# variables
folder_path = "TAI" 
re_map = {15: 1565.85, 40: 4175.60, 53: 5532.67}
plot_files = [15, 40, 53]
fs = 44100   

plt.figure(figsize=(10, 6))

for file_num in plot_files:
    re_val = re_map[file_num]
    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    # Read amplitude from single column
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()
    
    # Subtract mean for cleaner spectrum
    signal = signal - np.mean(signal)
    
    # Calculate PSD
    frequencies, psd = welch(signal, fs=fs, nperseg=8192)

    # Plot the results
    plt.semilogy(frequencies, psd, label=f"Re = {re_val:.2f}")

# Formatting for the paper
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density (V^2/Hz)")
plt.title("Figure 9: Spectral Evolution of TAI")

# ZOOM & SCALE FIXES
plt.xlim(0, 1000) 
plt.ylim(1e-12, 1e-2) # Sets the Y-axis from 10^-12 to 10^-2 as requested
plt.grid(True, which="both", ls="-", alpha=0.3)
plt.legend(title="Reynolds Number (Re)")
plt.tight_layout()

# Saving for git
plt.savefig("Figure_9_TAI_FrequencySpectrum_Fixed.png", dpi=300)
plt.show()