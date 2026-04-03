"""
this file is to simulate cumulative energy distribution for TAI
the graph describes how signal energy is distributed over frequency

we use FFT and compute cumulative energy in low frequency range
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# variables
folder_path = "TAI"

# mapping files to Reynolds number
re_map = {
    15: 1565.85, 
    45: 4697.55,  
    53: 5532.67
}

plt.figure(figsize=(10, 6))

# Define line styles
linestyles = ['-', '--', ':']

for idx, (file_num, re_val) in enumerate(re_map.items()):

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()

    # remove mean
    signal = signal - np.mean(signal)

    # sampling frequency
    fs = 44100

    # use only first 2 seconds
    signal = signal[:int(2 * fs)]

    # FFT
    fft_vals = np.fft.fft(signal)
    power = np.abs(fft_vals)**2

    freq = np.fft.fftfreq(len(signal), d=1/fs)

    # take only positive frequencies
    mask = freq >= 0
    freq = freq[mask]
    power = power[mask]

    # limit to 200–260 Hz
    mask = (freq >= 200) & (freq <= 260)
    freq = freq[mask]
    power = power[mask]

    # cumulative energy
    cum_energy = np.cumsum(power)
    cum_energy = cum_energy / cum_energy[-1]

    plt.plot(freq, cum_energy, linestyle=linestyles[idx], linewidth=2, label=f"Re = {re_val:.0f}")

plt.xlabel("Frequency (Hz)", fontsize=22)
plt.ylabel("Cumulative Energy Distribution", fontsize=22)
plt.xlim(200, 260)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

plt.grid(True, alpha=0.3)
plt.legend(fontsize=22)

plt.tight_layout()
plt.savefig("Figure_TAI_Cumulative_Energy.png", dpi=300)
plt.show()