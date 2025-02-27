# -*- coding: utf-8 -*-
"""
SING Gaze Project
Susanne Reisner

This script reads .xlsx look files from a directory, deletes rows with
looks <1s long and saves them to a new directory.
"""

import os
import pandas as pd
# glob

# Define paths
source_dir = "W:/hoehl/projects/sing/Behavioural_coding/Gaze/SingGaze_looks/all_mum_with_short_looks"
target_dir = "W:/hoehl/projects/sing/Behavioural_coding/Gaze/SingGaze_looks/"

# Ensure target directory exists
os.makedirs(target_dir, exist_ok=True)

# Process each matching XLSX file
for file in os.listdir(source_dir):
    if file.endswith("_mum.xlsx"):
        file_path = os.path.join(source_dir, file)
        df = pd.read_excel(file_path)
        
        # Filter out rows where 'Duration' is < 1
        df_filtered = df[df['Duration'] >= 1]
        
        # Save to target directory
        output_path = os.path.join(target_dir, file)
        df_filtered.to_excel(output_path, index=False)
        print(f"Processed and saved: {output_path}")
