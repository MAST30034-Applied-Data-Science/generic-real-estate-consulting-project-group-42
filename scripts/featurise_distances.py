"""
Categorises distances from continuous numerical values
"""

# Importing necessary libraries
import os
import pandas as pd

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/curated/"

# Read relevant data
distances = pd.read_csv(f"{dir_name}{relative_dir}all_distances.csv", index_col=0)
columns_to_categorise = ["Railway_Duration",  "Park_Duration", "Post_Office_Duration", "Primary_Duration", "Secondary_Duration",
                         "Railway_Distance",  "Park_Distance", "Post_Office_Distance", "Primary_Distance", "Secondary_Distance"]
processed_distances = distances[["Name", "Cost", "Coordinates", "Bed", "Bath", "Parking",
       "Property_Type", "Agency", "Postcode", "CBD_Duration", "Nearby_Schools"]]
processed_distances = processed_distances.reset_index()

# Categorise distance relative to the range of each variable
for col in columns_to_categorise:
    data = distances[col]
    dist_cat_dict = {}
    max_dist = max(data)
    for i in range(0, len(data)):
        cat = 0 
        if (data[i] > 0 and data[i] <= max_dist / 8):
            cat = 1
        elif (data[i] > max_dist / 8 and data[i] <= max_dist / 4):
            cat = 2
        elif (data[i] > max_dist / 4 and data[i] <= max_dist / 2):
            cat = 3
        elif (data[i] > max_dist / 2 and data[i] <= 3 * max_dist / 4):
            cat = 4
        elif (data[i] > 3 * max_dist / 4 and data[i] <= max_dist):
            cat = 5
        else:
            cat = 6

        dist_cat_dict[i] = cat
    
    processed_distances[col] = processed_distances["index"].map(dist_cat_dict)

# Save information
processed_distances = processed_distances.drop(["index"], axis=1)
processed_distances.to_csv(f"{dir_name}{relative_dir}categorised_distances.csv")

print("Completed featurising distances")