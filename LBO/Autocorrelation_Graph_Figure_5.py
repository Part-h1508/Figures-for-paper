"""
this file is to simulate the 5th figure (corrected)
the graph describes autocorrelation decay nearing LBO

updated based on prof feedback:
we now use a short segment instead of full signal
to capture local behaviour properly
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
df_details = pd.read_excel(main_file)

plt.figure(figsize=(10, 6))

# same operating points
plot_indices = [9, 3, 0]

for idx in plot_indices:

    row = df_details.iloc[idx]

    air_val = row['Air (SLPM)']
    phi_val = row['Equivalence ratio']
    
    file_name = os.path.join(folder_path, f"{int(air_val)}.xlsx")
    df_signal = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # sampling frequency
    fs = 1 / (df_signal['Time'].iloc[1] - df_signal['Time'].iloc[0])

    # remove mean
    signal = (df_signal['Amplitude'] - df_signal['Amplitude'].mean()).to_numpy()

    # 🔥 KEY FIX: use only first 2 seconds
    signal = signal[:int(2 * fs)]

    # autocorrelation
    corr = np.correlate(signal, signal, mode='full')
    center = corr.size // 2

    # 🔥 KEY FIX: shorter lag window (30 ms)
    max_lag = int(0.03 * fs)

    rxx = corr[center:center + max_lag] / corr[center]

    # optional smoothing (kept very light)
    rxx = np.convolve(rxx, np.ones(5)/5, mode='same')

    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_val:.3f}")

plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")

plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")

plt.tight_layout()
plt.savefig("Figure_5_LBO_Autocorrelation_FIXED.png", dpi=300)
plt.show()