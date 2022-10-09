"""
Merging distance datasets
"""

# Importing necessary libraries
import os
import pandas as pd
import warnings

from helper_functions import separate_dictionary

warnings.simplefilter(action="ignore", category=FutureWarning)

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/curated/"

# Read in data
amenities = pd.read_csv(f"{dir_name}{relative_dir}nearby_amenities.csv")
school = pd.read_csv(f"{dir_name}{relative_dir}school_distances.csv")

# Seperate and reformat distances and durations
amenities = separate_dictionary(amenities, "CBD_Distance")
amenities.rename({"distance":"CBD_Distance", "duration":"CBD_Duration"}, inplace=True, axis=1)
amenities = separate_dictionary(amenities, "Closest_Railway_Station")
amenities.rename({"distance":"Railway_Distance", "duration":"Railway_Duration"}, inplace=True, axis=1)
amenities = separate_dictionary(amenities, "Closest_Park")
amenities.rename({"distance":"Park_Distance", "duration":"Park_Duration"}, inplace=True, axis=1)
amenities = separate_dictionary(amenities, "Closest_Post_Office")
amenities.rename({"distance":"Post_Office_Distance", "duration":"Post_Office_Duration"}, inplace=True, axis=1)
school = separate_dictionary(school, "Primary_Distance")
school.rename({"distance":"Primary_Distance", "duration":"Primary_Duration"}, inplace=True, axis=1)
school = separate_dictionary(school, "Secondary_Distance")
school.rename({"distance":"Secondary_Distance", "duration":"Secondary_Duration"}, inplace=True, axis=1)

# Merge datasets
merged = amenities.merge(school)
merged = merged.drop("Unnamed: 0", axis="columns")
merged = merged.drop("Unnamed: 0.1", axis="columns")

# Final preprocessing of properties
merged = merged[merged["Cost"]>=100]
merged = merged[merged["Property_Type"] != "Carspace"]
merged = merged[merged["Property_Type"] != "Block of Units"]

merged = merged.replace(
    ["Penthouse", "New Apartments / Off the Plan"], 
    ["Apartment / Unit / Flat", "Townhouse"])

# Save file
merged = merged.reset_index(drop=True)
merged.to_csv(f"{dir_name}{relative_dir}all_distances.csv")

print("Completed merging distance datasets")