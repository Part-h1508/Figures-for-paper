# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os


# variables


# we will compare 3 distinct files
tgt_files = [15,35,53]

# declare a dict for rey numbers:
re_map = {
    15: 1565.85,
    35: 3653.65,
    53: 5532.67
}

# determine a fig size
plt.figure(figsize=(14,6))

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# now we dig thru the our target files
for i, file_num in enumerate(tgt_files):

    # set the file name
    filename = os.path.join(script_dir, str(file_num) + ".xlsx")

    # open the dataframe
    df1 = pd.read_excel(filename, header=None)
    
    # now we look for tgt values/ reyn in our opened files
    signal = df1.iloc[:,0].to_numpy()

    # now we normalize the signal
    # by normalize, we mean we divide by std deviation so all have a width of about 1
    # this can halp us ignore noise
    nor_signal = (signal - np.mean(signal)) / np.std(signal)

    # create a subplot
    plt.subplot(1,3,i+1)

    # we plot the histogram now, keeping in mind
    # bins=105 has been adjusted according to graph by trial and erro
    # keeping density
    plt.hist(nor_signal, bins=105, density=True, alpha=0.6, color='blue', label='1')

    # now we plot the gaussian curvv and a bell curvv
    x_axis = np.linspace(-4, 4, 100)
    plt.plot(x_axis, norm.pdf(x_axis, 0, 1), 'r--', linewidth=2, label='Gaussian')

    # formattting
    plt.title(f"Re: {re_map[file_num]}")
    plt.xlabel("Normalized amplitude")
    plt.ylim(0, 0.6) # Lock y-axis so we can compare easily
    plt.legend()
    plt.grid(True, alpha=0.3)

# show the plot
plt.suptitle("PDF Analysis: Transition from Random Noise to TAI (Sine Wave)", fontsize=16)
plt.tight_layout()
plt.show()