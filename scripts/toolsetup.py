"""
Creates the necessary databases and data structures required for the tool
"""

# Importing necessary libraries
import os
import json
import pandas as pd
from scipy.spatial import distance

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)

relative_dir_raw = "/data/raw/external/"
relative_dir_curated = "/data/curated/"

# Read in relevant data
postcodes = pd.read_csv(dir_name + relative_dir_curated + "unique_postcodes.csv", header=None, names = ["postcode"])
latlongs = pd.read_csv(dir_name + relative_dir_raw + "australian_postcodes/australian_postcodes.csv")

growth_rate_df = pd.read_csv(dir_name + relative_dir_curated + "growth_rate.csv")
affordability_df = pd.read_csv(dir_name + relative_dir_curated + "affordability.csv")
livability_df = pd.read_csv(dir_name + relative_dir_curated + "liveability.csv")

# Merging postcode data
latlongs = latlongs.loc[latlongs["state"]  == "VIC"]

merged = postcodes.merge(latlongs, on = "postcode", how = "left")
postcode_latlong = merged[["postcode", "lat", "long"]]
postcode_latlong = postcode_latlong.drop_duplicates(subset = ["postcode"])

# Merge all scores with postcodes
growth_rate_df.columns = ["Postcode", "Growth Rate"]
postcodes.columns = ["Postcode"]
final_df = postcodes.merge(growth_rate_df, on = "Postcode", how = "outer").merge(affordability_df, on="Postcode", how = "outer").merge(livability_df, on = "Postcode", how = "outer")

# Save merged dataset
final_df.to_csv(dir_name + relative_dir_curated + "growthrate_afford_live.csv")

print("Completed merging growth rate, affordability and liveability databases")

postcode_dict = {}

# Iterating through each postcode, calculate distance to each postcode and add the ten closest
for i in range(0, len(postcode_latlong)):
    inner_dict = {}
    current_postcode = postcode_latlong.iloc[i]
    curr_coords = [current_postcode["lat"], current_postcode["long"]]

    for j in range(0, len(postcode_latlong)):
        if j == i:
            continue
        else:
            # Calculate euclidean distance between current postcode and all others
            next_postcode = postcode_latlong.iloc[j]
            next_coords = [next_postcode["lat"], next_postcode["long"]]

            inner_dict[int(next_postcode["postcode"])] = distance.euclidean(curr_coords, next_coords)

    df = pd.DataFrame(list(inner_dict.items()), columns = ["postcode", "distance"])
    df = df.sort_values("distance")
    ten_closest = df.head(10)

    postcode_dict[int(current_postcode["postcode"])] = dict(zip(ten_closest["postcode"], ten_closest["distance"]))

# Save postcode distances
with open(dir_name + relative_dir_curated + "postcode_dists.json", "w") as outfile: 
    json.dump(postcode_dict, outfile)

print("Completed creating closest 10 postcode dictionary")

print("Completed tools database setup")