"""
this file is to simulate the 5th figure
the graph describes physical behaviour of the signal correlation
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
phi_name = "Equivalence ratio"

# open the main data file
df = pd.read_excel(main_file)

plt.figure(figsize=(10, 6))

# We ensure the order is consistent for the legend
# High Phi (Stable) -> Mid Phi (Transition) -> Low Phi (Blowout)
plot_indices = [9, 3, 0] 

for idx in plot_indices:
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # sampling frequency
    delta_t = df1['Time'].iloc[1] - df1['Time'].iloc[0]
    fs = 1 / delta_t
    
    # subtract mean to focus on fluctuations
    signal = df1['Amplitude'] - df1['Amplitude'].mean()
    signal = signal.to_numpy()
    
    # Efficient autocorrelation calculation
    n = len(signal)
    max_lag = int(0.1 * fs) # 100ms
    
    # Use full correlation and slice the positive lag side
    corr = np.correlate(signal, signal, mode='full')
    corr = corr[corr.size // 2:] 
    # Normalize such that Rxx(0) = 1.0
    rxx = corr[:max_lag] / corr[0]
    
    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_value:.3f}")

# formatting
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")
plt.title("Figure 5: Autocorrelation Decay nearing LBO (Corrected)")
plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

plt.savefig("Figure_5_LBO_Autocorrelation_Fixed.png", dpi=300)
plt.show()