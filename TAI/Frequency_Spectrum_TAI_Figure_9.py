"""
this file is to simulate the 9th figure
the graph describes the frequency peaks of TAI

Prof mentioned we should point the peak frequency
to highlight the dominant acoustic mode.
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

    # Plot the PSD curve
    plt.semilogy(frequencies, psd, label=f"Re = {re_val:.2f}")

    # ignore DC component when finding peak
    peak_index = np.argmax(psd[1:]) + 1
    peak_freq = frequencies[peak_index]
    peak_power = psd[peak_index]

    # mark the peak
    plt.plot(peak_freq, peak_power, 'ro', markersize=5)

    # draw vertical line at peak
    plt.axvline(peak_freq, linestyle='--', alpha=0.4)

    # label the peak slightly to the right and lower
    plt.text(peak_freq + 15, peak_power/3, f"{peak_freq:.1f} Hz")


# Formatting for the paper
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density (V^2/Hz)")

plt.xlim(0, 1000) 
plt.ylim(1e-12, 10)

plt.grid(True, which="both", ls="-", alpha=0.3)
plt.legend(title="Reynolds Number (Re)")

plt.tight_layout()

# Saving for git
plt.savefig("Figure_9_TAI_FrequencySpectrum.png", dpi=300)

plt.show()