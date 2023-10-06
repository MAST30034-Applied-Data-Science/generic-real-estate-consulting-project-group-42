"""
Renove duplicates for postcodes
"""

# Importing necessary libraries
import os
import pandas as pd

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = "/data/raw/external/"
relative_dir_curated = "/data/curated/"

# Postcode list
postcode = pd.read_csv(f"{dir_name}{relative_dir_raw}postcode.csv", header=None)
unique_postcode = postcode.iloc[:,0].drop_duplicates()
unique_postcode.to_csv(f"{dir_name}{relative_dir_curated}unique_postcodes.csv", index=False, header=False)

print("Completed preprocessing postcodes")