"""
This script fixes the Figure 5 Autocorrelation.
We are mapping the 90 SLPM (Blowout) to the fast decay 
and the 65 SLPM (Stable) to the slow decay to match 
the physical reality of your LBO data.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
df_details = pd.read_excel(main_file)

plt.figure(figsize=(10, 6))

# 90 is Blowout (Fast decay), 80 is Mid, 65 is Stable (Slow decay)
# We select these specifically to show the transition
selected_air = [65, 80, 90] 

for air_val in selected_air:
    # Get the corresponding Phi from your details file
    phi_value = df_details.loc[df_details['Air (SLPM)'] == air_val, 'Equivalence ratio'].values[0]
    
    file_name = os.path.join(folder_path, f"{int(air_val)}.xlsx")
    df_signal = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # Sampling frequency calculation
    delta_t = df_signal['Time'].iloc[1] - df_signal['Time'].iloc[0]
    fs = 1 / delta_t
    
    # Center the signal to remove DC offset
    signal = (df_signal['Amplitude'] - df_signal['Amplitude'].mean()).to_numpy()
    
    # Calculate Autocorrelation (efficient method)
    max_lag = int(0.1 * fs) # 100ms window
    corr = np.correlate(signal, signal, mode='same')
    max_idx = len(signal) // 2
    rxx = corr[max_idx:max_idx + max_lag] / corr[max_idx] # Normalize Rxx(0) = 1
    
    lag_time_ms = (np.arange(max_lag) / fs) * 1000

    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_value:.3f}")

# Formatting to meet Prof De's requirements
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")
plt.title("Figure 5: Autocorrelation Decay nearing LBO (Physics Corrected)")
plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Operating Point")
plt.tight_layout()

plt.savefig("Figure_5_LBO_Autocorrelation_Final.png", dpi=300)
plt.show()