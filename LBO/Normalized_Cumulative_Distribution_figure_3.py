"""
this file is to simulate the 3rd figure
the graph describes physical behaviour of the line
The fig includes:

Normalized cumulative duration of LBO precursor events at
different working conditions.

We find:
mean voltage --> blowout threshold at 72%
--> count data points below threshold
--> divide the count by total data points
"""

"""
Prof De reminded me that the LBO threshold should be 72%.
I am using the 'Fi/FI_LBO' column for the X-axis because
it shows the transition reaching the limit at 1.0.
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
x_axis_col = "Fi/FI_LBO" # using normalized equivalence ratio

# open the main data file
df = pd.read_excel(main_file)

# creating a list to store the calculated theta value
theta_values = []

# loop thru the data file to get the air values
for index, row in df.iterrows():
    # get the air value for the current row
    air_value = row[air_name]
    
    # open the file with the air value from the LBO folder
    file_name = os.path.join(folder_path, str(int(air_value)) + ".xlsx")
    df1 = pd.read_excel(file_name, header=None, names=['Time', 'Amplitude'])

    # calculate the mean amplitude (Q_bar)
    Q_bar = df1['Amplitude'].mean()

    # set the threshold at 72% of the mean amplitude
    threshold = 0.72 * Q_bar

    # count the number of data points below the threshold (flickers)
    count_below_threshold = (df1['Amplitude'] < threshold).sum()

    # calculate the total number of data points
    total_data_points = len(df1['Amplitude'])

    # check for division by zero
    if total_data_points > 0:
        # calculate theta
        theta = count_below_threshold / total_data_points
    else:
        theta = 0

    theta_values.append(theta)

# now we plot the theta values against the normalized equivalence ratio
plt.figure(figsize=(8, 6))
plt.plot(df[x_axis_col], theta_values, marker='o', linestyle='-', color='tab:red')

# labeling for the paper
plt.xlabel("Fi/FI_LBO")
plt.ylabel('Theta (Θ)')
plt.title('Figure 3: Threshold Intermittency (LBO)')
plt.grid(True, alpha=0.3)

# saving for git
plt.savefig("Figure_3_LBO_Theta.png", dpi=300)
plt.show()