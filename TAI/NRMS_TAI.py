"""
this file is to simulate NRMS for TAI
the graph describes fluctuation intensity of pressure signal

We plot NRMS vs Reynolds number

updated:
--> fixed NRMS definition for oscillatory signal
--> avoids division by near-zero mean
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

nrms_values = []
re_values = []

for file_num, re_val in re_map.items():

    file_name = os.path.join(folder_path, f"{file_num}.xlsx")
    
    df = pd.read_excel(file_name, header=None)
    signal = df[0].to_numpy()

    # NRMS
    mean_val = np.mean(signal)
    std_val = np.std(signal)

    # FIX: use mean absolute value instead of mean
    nrms = std_val / np.mean(np.abs(signal))

    nrms_values.append(nrms)
    re_values.append(re_val)

# plot
plt.figure(figsize=(8, 6))
plt.plot(re_values, nrms_values, marker='o')

plt.xlabel("Reynolds Number (Re)")
plt.ylabel("NRMS")

plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Figure_TAI_NRMS.png", dpi=300)
plt.show()