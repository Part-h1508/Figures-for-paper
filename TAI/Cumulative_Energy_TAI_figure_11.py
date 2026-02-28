# imports 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# variables
Freq = 44100
# we only need to compare the two extremes to see the difference
target_files = [15, 53]

# declaring a dict for reynolds number
re_map = {
    15: 1565.85, 
    53: 5532.67
}

# we set a time delay (tau) to shift the signal against itself
# we shift by roughly a quarter of a wave cycle (45 points for ~235Hz)
tau = 45 

# determine a fig size
plt.figure(figsize=(12, 6))

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# now we dig thru the our target files
for i, file_num in enumerate(target_files):
    # set the file name
    filename = os.path.join(script_dir, str(file_num) + ".xlsx")
    
    # open the data frame
    df = pd.read_excel(filename, header=None)

    # we look for target values in our opened files
    signal = df.iloc[:, 0].to_numpy()
    
    # we normalize the signal (mean 0, std 1)
    # this allows us to see the shape clearly on a fixed scale
    signal = (signal - np.mean(signal)) / np.std(signal)
    
    # now we create the phase space coordinates
    # X is the original signal, Y is the signal shifted by tau
    X = signal[:-tau]
    Y = signal[tau:]
    
    # plotting the graph
    plt.subplot(1, 2, i+1)
    
    # we use a scatter plot with very small dots (s=0.2)
    # this helps reveal the "Limit Cycle" or "Donut" structure
    plt.scatter(X, Y, s=0.2, alpha=0.5, color='black')
    
    # Formatting
    plt.title(f"Re: {re_map[file_num]}")
    plt.xlabel("Pressure (t)")
    plt.ylabel(f"Pressure (t + {tau/Freq:.4f}s)")
    
    # ensure the plot is a square so the donut isn't squashed
    plt.axis('equal') 
    plt.xlim(-4, 4)
    plt.ylim(-4, 4)
    plt.grid(True, alpha=0.3)

plt.suptitle("Phase Space Reconstruction", fontsize=16)
plt.tight_layout()
plt.savefig("Figure_11_TAI_PhaseSpaceReconstruction.png", dpi=300)
plt.show()
