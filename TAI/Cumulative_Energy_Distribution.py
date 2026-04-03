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

for file_num, re_val in re_map.items():

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

    # limit to 0–260 Hz
    mask = freq <= 100
    freq = freq[mask]
    power = power[mask]

    # cumulative energy
    cum_energy = np.cumsum(power)
    cum_energy = cum_energy / cum_energy[-1]

    plt.plot(freq, cum_energy, label=f"Re = {re_val:.0f}")

plt.xlabel("Frequency (Hz)")
plt.ylabel("Cumulative Energy")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_TAI_Cumulative_Energy.png", dpi=300)
plt.show()