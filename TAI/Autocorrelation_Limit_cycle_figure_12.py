"""
this file is to simulate autocorrelation for TAI
the graph describes temporal behaviour of pressure signal
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

folder_path = os.path.dirname(os.path.abspath(__file__))

re_map = {
    15: 1565.85,
    40: 4175.60,
    53: 5532.67
}

plt.figure(figsize=(10, 6))

for file_num, re_val in re_map.items():

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()

    # remove mean
    signal = signal - np.mean(signal)

    # compute max lag first (before expensive autocorrelation)
    fs = 44100  # same as your PSD
    max_lag = int(0.03 * fs)

    # autocorrelation using FFT (much faster than np.correlate)
    padded_size = 2 ** int(np.ceil(np.log2(len(signal) + max_lag)))
    fft_signal = np.fft.rfft(signal, n=padded_size)
    power = np.abs(fft_signal) ** 2
    autocorr = np.fft.irfft(power)[:len(signal)]
    
    rxx = autocorr[:max_lag] / autocorr[0]

    # create lag axis
    lag = np.arange(len(rxx)) / fs * 1000

    rxx = rxx[:max_lag]
    lag = lag[:max_lag]

    plt.plot(lag, rxx, label=f"Re = {re_val:.0f}")
    print(f"Processed Re = {re_val:.0f}, max autocorr = {rxx[0]:.2f}")

plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")

plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_TAI_Autocorrelation.png", dpi=300)
plt.show()