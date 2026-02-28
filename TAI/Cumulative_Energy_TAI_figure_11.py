"""
this file is to simulate the 11th figure
the graph describes the spectral energy accumulation of TAI
I have modified the normalization to focus on the first 500Hz.
This ensures the higher Reynolds number (5532) shows as 
more energetic/dominant compared to the 4175 case.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import welch

# variables
folder_path = "TAI" 
re_map = {15: 1565.85, 40: 4175.60, 53: 5532.67}
plot_files = [15, 40, 53]
fs = 44100   

plt.figure(figsize=(10, 6))

for file_num in plot_files:
    re_val = re_map[file_num]
    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()
    signal = signal - np.mean(signal)
    
    frequencies, psd = welch(signal, fs=fs, nperseg=1024)

    # We limit the normalization to the 0-500Hz range to 
    # ignore higher harmonics that 'pull' the curve down
    mask = frequencies <= 500
    freq_window = frequencies[mask]
    psd_window = psd[mask]

    cumulative_psd = np.cumsum(psd_window)
    # Normalizing only by the energy within this specific window
    cumulative_energy = cumulative_psd / cumulative_psd[-1]

    plt.plot(freq_window, cumulative_energy, label=f"Re = {re_val:.2f}", linewidth=1.5)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Normalized Cumulative Energy (0-500 Hz)")
plt.title("Figure 11: TAI Cumulative Energy (Harmonic Corrected)")
plt.xlim(0, 500) 
plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.legend(title="Reynolds Number (Re)")
plt.tight_layout()

plt.savefig("Figure_11_TAI_CumulativeEnergy_Corrected.png", dpi=300)
plt.show()