# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, skew
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

    # calculate skewness of the signal
    skew_val = skew(nor_signal)

    # check if distribution is left or right skewed
    if skew_val > 0:
        skew_type = "Right Skew"
    elif skew_val < 0:
        skew_type = "Left Skew"
    else:
        skew_type = "Symmetric"

    # print skewness value in terminal
    print(f"Re = {re_map[file_num]} | Skewness = {skew_val:.4f} ({skew_type})")

    # create a subplot
    plt.subplot(1,3,i+1)

    # we plot the histogram now, keeping in mind
    # bins=105 has been adjusted according to graph by trial and erro
    # keeping density
    plt.hist(nor_signal, bins=105, density=True, alpha=0.6, color='blue', label='PDF')

    # now we plot the gaussian curvv and a bell curvv
    x_axis = np.linspace(-4, 4, 100)
    plt.plot(x_axis, norm.pdf(x_axis, 0, 1), 'r--', linewidth=2, label='Gaussian')

    # formattting
    plt.title(f"Re: {re_map[file_num]}", fontsize=22)
    plt.xlabel("Normalized amplitude", fontsize=22)
    plt.ylabel("Probability Density", fontsize=22)
    plt.ylim(0, 0.6) # Lock y-axis so we can compare easily
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # annotate skewness value on the plot
    plt.text(-3.5, 0.5, f"Skew = {skew_val:.3f}", fontsize=18)

    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

# adjust spacing
plt.tight_layout()

# save figure
plt.savefig("Figure_13_TAI_Bimodal_limit_cycle_oscillation.png", dpi=300)

# show the plot
plt.show()