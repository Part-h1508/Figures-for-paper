"""
Autocorrelation plot for LBO (corrected)

Fixes applied:
- Proper normalization so r(0) = 1
- No smoothing that distorts zero-lag value
- Uses short segment for local behaviour
- Clear and correct implementation
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    "font.size": 22,
    "axes.labelsize": 22,
    "xtick.labelsize": 22,
    "ytick.labelsize": 22,
    "legend.fontsize": 22
})

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
    dt = df_signal['Time'].iloc[1] - df_signal['Time'].iloc[0]
    fs = 1 / dt

    # remove mean
    signal = df_signal['Amplitude'].to_numpy()
    signal = signal - np.mean(signal)

    # use only first 2 seconds
    N = int(2 * fs)
    signal = signal[:N]

    # compute autocorrelation (normalized)
    corr = np.correlate(signal, signal, mode='full')
    center = len(corr) // 2

    # normalize → ensures r(0) = 1
    corr = corr / corr[center]

    # lag window (30 ms)
    max_lag = int(0.03 * fs)
    rxx = corr[center:center + max_lag]

    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_val:.3f}")

plt.xlabel("Lag Time (ms)", fontsize=22)
plt.ylabel("Autocorrelation Coefficient", fontsize=22)

plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)", fontsize=16, title_fontsize=16)

plt.tight_layout()
plt.savefig("Figure_5_LBO_Autocorrelation_FIXED_again.png", dpi=300)
plt.show()