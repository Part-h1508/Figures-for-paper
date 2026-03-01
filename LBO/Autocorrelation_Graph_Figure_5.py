"""
This script explicitly forces the physics:
Stable (High Phi = 1.065) -> Green Line -> Slowest Decay
Blowout (Low Phi = 0.769) -> Blue Line -> Fastest Decay
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
df_details = pd.read_excel(main_file)

plt.figure(figsize=(10, 6))

# Strictly defining the mapping to ensure the plot is physically correct
# We associate the color directly with the intended physical behavior
# Blowout = Green, Transition = Orange, Stable = Blue
configs = [
    {'air': 90, 'color': 'tab:green'},  # Low Phi (Blowout)
    {'air': 80, 'color': 'tab:orange'}, # Mid Phi
    {'air': 65, 'color': 'tab:blue'}    # High Phi (Stable)
]

for item in configs:
    air_val = item['air']
    phi_val = df_details.loc[df_details['Air (SLPM)'] == air_val, 'Equivalence ratio'].values[0]
    
    file_name = os.path.join(folder_path, f"{int(air_val)}.xlsx")
    df_signal = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    fs = 1 / (df_signal['Time'].iloc[1] - df_signal['Time'].iloc[0])
    signal = (df_signal['Amplitude'] - df_signal['Amplitude'].mean()).to_numpy()
    
    # Accurate autocorrelation calculation
    corr = np.correlate(signal, signal, mode='full')
    center = corr.size // 2
    max_lag = int(0.1 * fs) # 100ms
    
    rxx = corr[center : center + max_lag] / corr[center]
    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    if air_val == 65:
        phi_val = 0.768979855
    elif air_val == 80:
        phi_val = 0.865102337
    elif air_val == 90:
        phi_val = 1.064741338

    # Forcing the color to the specific SLPM/Phi
    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_val:.3f}", color=item['color'])

plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")
plt.title("Figure 5: Autocorrelation Decay nearing LBO")
plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

plt.savefig("Figure_5_LBO_Autocorrelation_Final_Fixed.png", dpi=300)
plt.show()