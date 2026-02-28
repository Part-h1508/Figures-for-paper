"""
this file is to simulate the 5th figure
the graph describes physical behaviour of the signal correlation
The fig includes:

Autocorrelation curves for LBO.
It shows how the signal's self-similarity decays over time.

We find:
Rxx(tau) --> high correlation for stable periodic signals
--> fast decay to zero near LBO
--> loss of "memory" in the flame as it becomes chaotic
"""

"""
Prof De wants to see the loss of correlation.
In stable conditions, the signal repeats itself.
In LBO, the flickering is random, so the 
autocorrelation drops quickly. I am plotting 
lags up to 100ms.
"""

# imports
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

# setting up the plot
plt.figure(figsize=(10, 6))

# using the same indices: 90 SLPM (Stable), 80 (Transition), 65 (LBO)
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
    
    # center the signal (subtract mean) for proper correlation
    signal = df1['Amplitude'] - df1['Amplitude'].mean()
    
    # calculate autocorrelation using numpy.correlate
    # we normalize it so that at lag=0, Rxx=1
    n = len(signal)
    lags = np.arange(0, int(0.1 * fs)) # checking up to 100ms lag
    
    # compute correlation for the selected lags
    rxx = np.array([np.corrcoef(signal[:n-lag], signal[lag:])[0,1] for lag in lags])
    
    # time axis for lags in ms
    lag_time_ms = (lags / fs) * 1000

    # plot the autocorrelation vs lag time
    plt.plot(lag_time_ms, rxx, label=f"Φ = {phi_value:.3f}")

# formatting for the paper per Prof De's feedback
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")
plt.title("Figure 5: Autocorrelation Decay nearing LBO")
plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

# saving for git
plt.savefig("Figure_5_LBO_Autocorrelation.png", dpi=300)
plt.show()

"""
The blue line is lowest eq ratio which shows a stable decay
which means the signal is highly correlated to its past signals
it has a strong prediction rythm

The orange line is middle eq ratio which shows somewhat faster 
drop which means the flame is becoming chaotic and is not 
following the past trends of previous osicllations making it less correalted

The green line is highest eq ratio which is the blowout precursor rate 
which shows that the correlation crashed to zero wildly which shows
that the flame is intermittent and unstable

"""