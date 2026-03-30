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
folder_path = "."
re_map = {15: 1565.85, 40: 4175.60, 53: 5532.67}
plot_files = [15, 40, 53]
fs = 44100

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "legend.fontsize": 14
})

plt.figure(figsize=(10, 6))

for file_num in plot_files:
    re_val = re_map[file_num]

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    df = pd.read_excel(file_name, header=None)

    signal = df[0].to_numpy()
    signal = signal.copy()
    signal -= np.mean(signal)

    frequencies, psd = welch(signal, fs=fs, nperseg=8192)

    plt.semilogy(frequencies, psd, label=f"Re = {re_val:.2f}")

    peak_index = np.argmax(psd[1:]) + 1
    peak_freq = frequencies[peak_index]
    peak_power = psd[peak_index]

    plt.plot(peak_freq, peak_power, 'ro')

    plt.text(peak_freq + 20, peak_power * 0.5,
             f"{peak_freq:.1f} Hz", fontsize=14)

plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD (V²/Hz)")

plt.xlim(0, 1000)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_9_TAI_FrequencySpectrum.png", dpi=300)
plt.show()