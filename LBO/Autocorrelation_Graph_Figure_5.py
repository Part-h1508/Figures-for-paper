"""
this file is to simulate the 5th figure
the graph describes the autocorrelation decay nearing LBO

Earlier version manually forced the physics by assigning colors
to specific air flow values. That approach has been removed.

Now the curves are plotted directly from the data so that the
ordering of decay behaviour is determined by the actual signals.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
df_details = pd.read_excel(main_file)

plt.figure(figsize=(10, 6))

# selecting the same three operating points used earlier
# index 9 (90 SLPM) -> Φ ≈ 0.769
# index 3 (80 SLPM) -> Φ ≈ 0.865
# index 0 (65 SLPM) -> Φ ≈ 1.065
plot_indices = [9, 3, 0]

for idx in plot_indices:

    row = df_details.iloc[idx]

    air_val = row['Air (SLPM)']
    phi_val = row['Equivalence ratio']
    
    file_name = os.path.join(folder_path, f"{int(air_val)}.xlsx")
    df_signal = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # sampling frequency
    fs = 1 / (df_signal['Time'].iloc[1] - df_signal['Time'].iloc[0])

    # remove mean from signal
    signal = (df_signal['Amplitude'] - df_signal['Amplitude'].mean()).to_numpy()
    
    # autocorrelation calculation
    corr = np.correlate(signal, signal, mode='full')

    center = corr.size // 2

    # look at first 100 ms of lag
    max_lag = int(0.1 * fs)
    
    rxx = corr[center:center + max_lag] / corr[center]

    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_val:.3f}")

plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")

plt.axhline(0, color='black', linewidth=1, alpha=0.5)

plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

plt.savefig("Figure_5_LBO_Autocorrelation.png", dpi=300)
plt.show()