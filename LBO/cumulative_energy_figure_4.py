"""
this file is to simulate the 4th figure
the graph describes physical behaviour of the spectral energy
The fig includes:

Cumulative energy curves for LBO.
It shows how energy accumulates across the frequency range.

We find:
PSD integration --> cumulative energy from 0 to fs/2
--> stable flames have energy spread to high frequencies
--> unstable flames (near LBO) reach 90% energy much faster
--> dominant energy shifts below 50 Hz
"""

"""
Prof De wants to see the shift in energy.
I am calculating the cumulative sum of the PSD.
If the curve is steep at the start, it means 
all the 'power' is in the low-frequency rumble.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.signal import welch

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
phi_name = "Equivalence ratio"

# open the main data file
df = pd.read_excel(main_file)

# setting up the plot
plt.figure(figsize=(10, 6))

# using the same indices for consistency: 90 SLPM (Stable), 80 (Transition), 65 (LBO)
plot_indices = [9, 3, 0]

# loop thru the selected data points
for idx in plot_indices:
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    # open the file from the LBO folder
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # calculate sampling frequency
    delta_t = df1['Time'].iloc[1] - df1['Time'].iloc[0]
    fs = 1 / delta_t
    
    # calculate PSD
    frequencies, psd = welch(df1['Amplitude'].values, fs=fs, nperseg=4096)

    # calculate cumulative energy (normalized to 1.0)
    cumulative_psd = np.cumsum(psd)
    cumulative_energy = cumulative_psd / cumulative_psd[-1]

    # plot the cumulative energy vs frequency
    plt.plot(frequencies, cumulative_energy, label=f"Φ = {phi_value:.3f}", linewidth=1.5)

# formatting for the paper
plt.xlabel("Frequency (Hz)")
plt.ylabel("Normalized Cumulative Energy")
plt.title("Figure 4: Cumulative Energy Shift towards LBO")

# focus on the 0-200 Hz range to see the 'step' in energy
plt.xlim(0, 200) 
plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

# saving for git
plt.savefig("Figure_4_LBO_CumulativeEnergy.png", dpi=300)
plt.show()