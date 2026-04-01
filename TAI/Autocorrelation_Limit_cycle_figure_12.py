"""
this file is to simulate autocorrelation for TAI
the graph describes temporal behaviour of pressure signal

updated:
--> using Excel CORREL style (pearson correlation)
--> using short segment (2 sec)
--> removed unstable high lag region
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# variables
folder_path = "TAI"

# mapping files to Reynolds number
re_map = {
    15: 1565.85, 
    20: 2087.80, 
    25: 2609.75, 
    30: 3131.70, 
    35: 3653.65, 
    40: 4175.60, 
    45: 4697.55, 
    50: 5219.50, 
    53: 5532.67
}

plt.figure(figsize=(10, 6))

for file_num, re_val in re_map.items():

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()

    # sampling frequency (assume uniform time step)
    # if time column exists, use that instead
    fs = 44100  # keep same as your experiment

    # use only first 2 seconds
    signal = signal[:int(2 * fs)]

    # autocorrelation
    acf = []

    max_lag = 15
    min_points = 50

    for k in range(max_lag + 1):

        if k == 0:
            x1 = signal
            x2 = signal
        else:
            x1 = signal[:-k]
            x2 = signal[k:]

        if len(x1) < min_points:
            break

        r = np.corrcoef(x1, x2)[0, 1]
        acf.append(r)

    acf = np.array(acf)
    acf = np.nan_to_num(acf)

    lag = np.arange(len(acf))

    plt.plot(lag, acf, label=f"Re = {re_val:.0f}")

plt.xlabel("Lag")
plt.ylabel("Autocorrelation Function")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_TAI_Autocorrelation_ex.png", dpi=300)
plt.show()