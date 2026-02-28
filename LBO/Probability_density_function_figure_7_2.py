"""
this file is to simulate figure 7.2
the graph describes the statistical distribution (PDF)
The fig includes:

Probability Density Functions for three equivalence ratios.
It shows how the signal's probability 'spreads' near LBO.

We find:
Stable (0.769) --> narrow, symmetric Gaussian-like peak
Transition (0.865) --> PDF starts to widen and flatten
Near LBO (1.065) --> very broad, skewed distribution reflecting 
the presence of large-amplitude precursor events (flickers).
"""

"""
Prof De wants to see how the signal distribution changes.
In stable cases, fluctuations are tiny, so the PDF is tight.
Near blowout, the 'dips' in the signal create a long tail 
in the distribution.

IMPORTANT FIX:
Gaussian must be fitted on normalized signal (not raw signal),
otherwise it appears shifted because histogram uses normalized data.
"""

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import norm

# variables
folder_path = "LBO" 
main_file = os.path.join(folder_path, "Data details.xlsx")
air_name = "Air (SLPM)"
phi_name = "Equivalence ratio"

# open the main data file
df = pd.read_excel(main_file)

# setting up the plot
plt.figure(figsize=(10, 6))

# using the same indices for the story: 90, 80, and 65 SLPM
plot_indices = [9, 3, 0]
colors = ['tab:blue', 'tab:orange', 'tab:green']

# loop thru the selected data points
for i, idx in enumerate(plot_indices):
    
    row = df.iloc[idx]
    air_value = row[air_name]
    phi_value = row[phi_name]
    
    # open the file from the LBO folder
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # signal processing - normalize by mean for easier comparison
    signal = df1['Amplitude'].to_numpy()
    mean_val = np.mean(signal)
    normalized_signal = signal / mean_val

    """
    For the stable case (idx == 9), we also plot theoretical Gaussian.
    We fit Gaussian on normalized signal so it aligns with histogram scale.
    """
    if idx == 9:
        mu, std = norm.fit(normalized_signal)   # fit normalized data
        
        x = np.linspace(
            min(normalized_signal),
            max(normalized_signal),
            200
        )
        
        p = norm.pdf(x, mu, std)
        
        plt.plot(
            x, p,
            'k--',
            linewidth=1.5,
            label='Theoretical Gaussian'
        )
    
    # calculate and plot the PDF using a density histogram
    # density=True ensures total area = 1 (proper PDF)
    plt.hist(
        normalized_signal,
        bins=100,
        density=True,
        histtype='step',
        linewidth=2,
        label=f"Φ = {phi_value:.3f}",
        color=colors[i]
    )

# formatting for the paper per Prof De's feedback
plt.xlabel("Normalized Amplitude (I / I_mean)")
plt.ylabel("Probability Density")
plt.title("Figure 7.2: PDF Evolution nearing LBO")
plt.grid(True, alpha=0.3)
plt.legend(title="Equivalence Ratio (Φ)")
plt.tight_layout()

# saving for git
plt.savefig("Figure_7_2_LBO_PDF.png", dpi=300)
plt.show()