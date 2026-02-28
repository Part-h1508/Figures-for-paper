"""
this file is to simulate the 2nd figure
the graph describes physical behaviour of the frequencies
The fig includes:

Frequency spectrum (PSD) for LBO precursors.
The legend shows Equivalence ratio (Phi) instead of Airflow.

We find:
Sampling frequency --> calculated from delta_t in time column
Low frequency rumble --> dominant peaks appear below 50 Hz
--> As Phi increases, energy shifts to low frequencies
--> Clear spectral peak near LBO indicating periodic flickering
"""

"""
Prof De mentioned the frequency spectrum was wrong.
He wants Phi in the legend and a focus on LBO precursors.
I am zooming the X-axis to 100Hz to show the rumble 
that corresponds to the humps seen in the time series.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch
import numpy as np
import os

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
phi_name = "Equivalence ratio"

# open the main data file
df = pd.read_excel(main_file)

# setting up the plot
plt.figure(figsize=(10, 6))

# using the same indices as Figure 1 for consistency
# index 9 (90 SLPM), index 3 (80 SLPM), index 0 (65 SLPM)
plot_indices = [9, 3, 0]

# loop thru the selected data points
for idx in plot_indices:
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    # open the file from the LBO folder
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # calculate sampling frequency from the data
    delta_t = df1['Time'].iloc[1] - df1['Time'].iloc[0]
    fs = 1 / delta_t
    
    # calculate the power spectral density using welch method
    # nperseg=4096 gives us the resolution needed to see low-freq peaks
    frequencies, psd = welch(df1['Amplitude'].values, fs=fs, nperseg=4096)

    # plot the frequency against PSD
    # we use semilogy to see the differences in energy levels clearly
    plt.semilogy(frequencies, psd, label=f"Φ = {phi_value:.3f}")

# now we format the graph for the paper
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density (PSD)")
plt.title("Figure 2: Frequency Spectrum (LBO Precursors)")

# Prof De requested to show precursors, so we zoom into 0-100 Hz
plt.xlim(0, 100) 
plt.grid(True, which="both", ls="-", alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

# saving the figure for git
plt.savefig("Figure_2_LBO_FrequencySpectrum.png", dpi=300)
plt.show()