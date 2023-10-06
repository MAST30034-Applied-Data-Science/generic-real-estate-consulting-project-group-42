"""
Cleans scraped property data
"""

# Importing necessary libraries
import os
import pandas as pd

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/raw/"

# Load data
properties = pd.read_csv(f"{dir_name}{relative_dir}property_data.csv", index_col=0)

# Reformat costs without commas
properties["Cost"] = properties["Cost"].str.replace(",", "")

# Change null values to numeric zero
properties["Bed"] = properties["Bed"].replace("−", 0)
properties["Bath"] = properties["Bath"].replace("−", 1)
properties["Parking"] = properties["Parking"].replace("−", 0)

# Null postcodes and coordinates are invalid rows
properties = properties[~properties["Postcode"].isna()]
properties = properties[properties["Coordinates"]!="[0.0, 0.0]"]

# Convert column types
properties["Cost"] = properties["Cost"].astype(float)
properties["Bed"] = properties["Bed"].astype(int)
properties["Bath"] = properties["Bath"].astype(int)
properties["Parking"] = properties["Parking"].astype(int)
properties["Postcode"] = properties["Postcode"].astype(int).astype(str)

# Edit cost parameters properties
properties = properties[properties["Cost"] != 0]
properties = properties[properties["Cost"] <= 20000]

# Save data
relative_dir = "/data/curated/"
new = properties.reset_index(drop=True)
new.to_csv(f"{dir_name}{relative_dir}properties_processed.csv")
new.to_json(f"{dir_name}{relative_dir}properties_processed.json")

print("Completed preprocessing properties")