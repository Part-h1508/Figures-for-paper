"""
this file is to simulate figure 7.1
the graph describes the fluctuation intensity (NRMS)
The fig includes:

NRMS values plotted against Normalized Equivalence Ratio.
This matches Fig. 8 from the Yi and Gutmark paper.

We find:
NRMS = std(amplitude) / mean(amplitude)
--> stable flame has very low NRMS (below 0.15)
--> as we hit 1.0 (LBO), NRMS spikes toward 0.45
"""

"""
I am using the 'Fi/FI_LBO' column for the X-axis 
to show the spike at the 1.0 limit. This is the 
primary tool the paper suggests for LBO prediction.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
x_axis_col = "Fi/FI_LBO"

# open the main data file
df = pd.read_excel(main_file)

# list to store NRMS
nrms_values = []

# loop thru to calculate NRMS for each condition
for index, row in df.iterrows():
    air_value = row[air_name]
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # calculate NRMS: standard deviation divided by the mean
    mean_amp = df1['Amplitude'].mean()
    std_amp = df1['Amplitude'].std()
    nrms = std_amp / mean_amp
    
    nrms_values.append(nrms)

# plot the NRMS curve
plt.figure(figsize=(8, 6))
plt.plot(df[x_axis_col], nrms_values, marker='s', color='tab:blue', label='Experimental NRMS')

plt.xlabel("Normalized Equivalence Ratio (Φ/Φ_lbo)")
plt.ylabel('NRMS')
plt.title('Figure 7.1: NRMS vs Normalized Equivalence Ratio')
plt.grid(True, alpha=0.3)
plt.savefig("Figure_7_1_NRMS.png", dpi=300)
plt.show()