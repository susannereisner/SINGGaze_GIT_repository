# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 16:35:16 2025

@author: reisners97

This script creates one big file out of individual files under the same header column.
We also add a column for the latency between looks within one condition.
"""

import pandas as pd
import glob

# Define the directory containing your files
directory = "W:/hoehl/projects/sing/Behavioural_coding/Gaze/SingGaze_looks/"
output_directory = "W:/hoehl/projects/sing/Logs/"

# Get all relevant files (adjust pattern if needed)
file_list = glob.glob(directory + "*_mum.xlsx")

# Initialize an empty list to store DataFrames
df_list = []

# Read and store each file
for file in file_list:
    df = pd.read_excel(file)  # Read file
    df_list.append(df)  # Append to list

# Concatenate all DataFrames into one
mum_looks = pd.concat(df_list, ignore_index=True)

# Save to CSV
output_file = output_directory + "SINGGaze_mum_looks.csv"
mum_looks.to_csv(output_file, index=False)

print(f"Files merged and saved as {output_file}")




'''
Add a column calculating the latency between 2 looks, if:
    - same ID
    - same condition
'''


# Sort the data by ID, Condition, and Onset to ensure rows are in the correct order
mum_looks_latency = mum_looks.sort_values(by=['ID', 'Condition', 'Onset']).reset_index(drop=True)

# Create a new column for latency
mum_looks_latency['Latency'] = None

# Loop through the DataFrame to calculate latency
for i in range(len(mum_looks_latency) - 1):
    if mum_looks_latency.loc[i, 'ID'] == mum_looks_latency.loc[i + 1, 'ID'] and mum_looks_latency.loc[i, 'Condition'] == mum_looks_latency.loc[i + 1, 'Condition']:
        mum_looks_latency.loc[i, 'Latency'] = mum_looks_latency.loc[i + 1, 'Onset'] - mum_looks_latency.loc[i, 'Offset']

# Save to CSV

mum_looks_latency.to_csv(output_file, index=False)
print(f"Updated file with latency saved as {output_file}")
