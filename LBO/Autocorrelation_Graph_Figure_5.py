"""
this file is to simulate autocorrelation for LBO (final corrected)
the graph describes temporal behaviour of the flame signal

updated based on prof feedback:
--> using Excel CORREL style (pearson correlation)
--> using short segment (2 sec)
--> removed unstable high lag region
--> fixed axis label and font size
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

folder_path = "LBO"
main_file = os.path.join(folder_path, "Data details.xlsx")
df_details = pd.read_excel(main_file)

# increase font size
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 16,
    'legend.fontsize': 12
})

plt.figure(figsize=(10, 6))

# same operating points
plot_indices = [9, 3, 0]

for idx in plot_indices:

    row = df_details.iloc[idx]

    air_val = row['Air (SLPM)']
    phi_val = row['Equivalence ratio']
    
    file_name = os.path.join(folder_path, f"{int(air_val)}.xlsx")
    df_signal = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    time = df_signal['Time'].to_numpy()
    signal = df_signal['Amplitude'].to_numpy()

    # sampling frequency
    fs = 1 / (time[1] - time[0])

    # use only first 2 seconds
    signal = signal[:int(2 * fs)]

    # autocorrelation (Excel CORREL style)
    acf = []

    max_lag = 15
    min_points = 50   # avoid weird tail

    for k in range(max_lag + 1):

        if k == 0:
            x1 = signal
            x2 = signal
        else:
            x1 = signal[:-k]
            x2 = signal[k:]

        # stop if too few points
        if len(x1) < min_points:
            break

        r = np.corrcoef(x1, x2)[0, 1]
        acf.append(r)

    acf = np.array(acf)
    acf = np.nan_to_num(acf)

    lag = np.arange(len(acf))

    plt.plot(lag, acf, label=f"Φ = {phi_val:.3f}")

plt.xlabel("Lag")
plt.ylabel("Autocorrelation Function")

plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")

plt.tight_layout()
plt.savefig("Figure_LBO_Autocorrelation_FINAL.png", dpi=300)
plt.show()