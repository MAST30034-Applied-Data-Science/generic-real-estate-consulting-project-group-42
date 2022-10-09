"""
Records the distance of the closest park, post office and railway station
"""

# Importing necessary libraries
import json
import os
import pandas as pd

from dotenv import load_dotenv
from helper_functions import find_poi, get_route

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
output_dir = "/data/curated/"

# Load tokens
load_dotenv()
num_tokens = 34
tokens = []
for i in range(1,num_tokens+1):
    token = os.environ.get(f"token_{i}")
    tokens.append(token)

# Decalre variables
melbourne_cbd = [144.9631, -37.8136] # taken from google maps 
park = 208
post = 370
train = 604
buffer_size = 2000   # radius of 2km (highest possible)

# Create dicts
cbd_dict = {}
category_ids = [park, post, train]
amenities_dict = {}

# Flag manual inputs
manual_cbd = [10497, 10561, 10581, 10590, 10591, 11129, 11728, 11729, 12797]
manual_parks = [10561, 10581, 10590, 10591, 12047, 12715, 12717, 12797]
manual_ptv = [10561, 10581, 10590, 10591]

# Read apartment data
property_data = json.load(open(f"{dir_name}{output_dir}properties_processed.json"))
# Read existing file (since more calls to poi than tokens)
if os.path.exists(f"{dir_name}{output_dir}nearby_amenities.json"):
    amenities_dict = json.load(open(f"{dir_name}{output_dir}nearby_amenities.json"))

# Find cbd routes
for token in tokens:
    # Set x and y
    x = len(cbd_dict)
    y = len(cbd_dict)+500 # 2000-3*500 for routes across script
    if y > len(property_data["Coordinates"].keys()):
        y = len(property_data["Coordinates"].keys())

    for index in range(x,y):
        backwards = list(map(float,property_data["Coordinates"][str(index)][1:-1].split(",")))
        coords = [[backwards[1], backwards[0]]]
        
        # Find route
        if index in manual_cbd:
            info = 0
        else:
            info = get_route(coords, melbourne_cbd, token)

    # Add information
    cbd_dict[str(index)] = info

# Find pois
for token in tokens:    
    for category in category_ids:
        # Set x and y
        x = len(amenities_dict[category])
        y = len(amenities_dict[category])+500 # Poi api limit
        if y > len(property_data["Coordinates"].keys()):
            y = len(property_data["Coordinates"].keys())

        for index in range(x,y):
            if (category == park)&(index in manual_parks):
                amenities_dict[category][str(index)] = 0
            elif (category == train)&(index in manual_ptv):
                amenities_dict[category][str(index)] = 0
            else:
                amenities_dict = find_poi(property_data, index, token, buffer_size, category, amenities_dict)

# Manual input
if os.path.exists(f"{dir_name}{output_dir}nearby_amenities.json"): # ie second/last run so as to not affect lengths
    cbd_dict["10497"] = {'distance': 295100.0, 'duration': 13050.05}
    cbd_dict["10561"] = {'distance': 36300.0, 'duration': 2070.0}
    amenities_dict[park]["10561"] = {'distance': 1200.0, 'duration': 240.0}
    amenities_dict[train]["10561"] = {'distance': 1300.0, 'duration': 180.0}
    cbd_dict["10581"] = {'distance': 36200.0, 'duration': 2016.0}
    amenities_dict[park]["10581"] = {'distance': 1000.0, 'duration': 240.0}
    amenities_dict[train]["10581"] = {'distance': 1100.0, 'duration': 120.0}
    cbd_dict["10590"] = {'distance': 36250.0, 'duration': 2010.0}
    amenities_dict[park]["10590"] = {'distance': 800.0, 'duration': 180.0}
    amenities_dict[train]["10590"] = {'distance': 900.0, 'duration': 120.0}
    cbd_dict["10591"] = {'distance': 36300.0, 'duration': 2070.0}
    amenities_dict[park]["10591"] = {'distance': 1200.0, 'duration': 240.0}
    amenities_dict[train]["10591"] = {'distance': 1300.0, 'duration': 180.0}
    cbd_dict["11129"] = {'distance': 320900.0, 'duration': 14124.0}
    cbd_dict["11728"] = {'distance': 226000.0, 'duration': 9336.0}
    cbd_dict["11729"] = {'distance': 201400.0, 'duration': 8430}
    amenities_dict[park]["12047"] = {'distance': 3200.0, 'duration': 360.0}
    amenities_dict[park]["12715"] = {'distance': 1300.0, 'duration': 180.0}
    amenities_dict[park]["12717"] = {'distance': 1300.0, 'duration': 180.0}
    cbd_dict["12797"] = {'distance': 82700.0, 'duration': 66.3}
    amenities_dict[park]["12797"] = {'distance': 1600.0, 'duration': 180.0}

# Write json
property_data["Closest_Park"] = amenities_dict[park]
property_data["Closest_Post_Office"] = amenities_dict[post]
property_data["Closest_Railway_Station"] = amenities_dict[train]
property_data["CBD_Distance"] = cbd_dict

json.dump(property_data, open(f"{dir_name}{output_dir}nearby_amenities.json", "w"))

# Write csv
data = pd.read_json(f"{dir_name}{output_dir}nearby_amenities.json")
data.to_csv(f"{dir_name}{output_dir}nearby_amenities.csv")

print("Completed finding POI and CBD distances")