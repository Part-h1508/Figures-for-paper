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

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch
import numpy as np
import os

plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14
})

folder_path = "."
main_file = os.path.join(folder_path, "Data details.xlsx")

df = pd.read_excel(main_file)

plt.figure(figsize=(10, 6))

plot_indices = [9, 3, 0]

for idx in plot_indices:
    row = df.iloc[idx]
    air_value = row["Air (SLPM)"]
    phi_value = row["Equivalence ratio"]

    file_name = os.path.join(folder_path, f"{int(air_value)}.xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    delta_t = df1['Time'].iloc[1] - df1['Time'].iloc[0]
    fs = 1 / delta_t

    frequencies, psd = welch(df1['Amplitude'].values, fs=fs, nperseg=4096)

    plt.semilogy(frequencies, psd, label=f"Φ = {phi_value:.3f}")

    if abs(phi_value - 0.769) < 0.001:
        peak_index = np.argmax(psd[1:]) + 1
        peak_freq = frequencies[peak_index]
        peak_power = psd[peak_index]

        plt.plot(peak_freq, peak_power, 'ro')

        plt.annotate(
            f"{peak_freq:.1f} Hz",
            xy=(peak_freq, peak_power),
            xytext=(peak_freq + 50, peak_power * 3),
            fontsize=14,
            arrowprops=dict(arrowstyle="->")
        )

plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD")
plt.xlim(0, 100)
plt.grid(True, alpha=0.3)
plt.legend(title="Φ")

plt.tight_layout()
plt.savefig("Figure_2_LBO_FrequencySpectrum.png", dpi=300)
plt.show()