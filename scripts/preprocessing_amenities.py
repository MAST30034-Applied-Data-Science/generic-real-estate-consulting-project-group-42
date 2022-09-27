"""
Records the distance of the closest park, post office and railway station
"""

import json
import os
import pandas as pd

from dotenv import load_dotenv
from helper_functions import find_poi

## find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
output_dir = '/data/curated/'

## set variables
load_dotenv()
tokens = []
for i in range(1,35): # number of tokens
    token = os.environ.get(f'token_{i}')
    tokens.append(token)
category_ids = [280, 370, 604] # park, post office, railway station
buffer_size = 2000   # radius of 2km (highest possible)
amenities_dict = {}

## read apartment data
property_data = json.load(open(f"{dir_name}{output_dir}properties_processed.json"))
## read existing file (since more calls to poi than tokens)
if os.path.exists(f"{dir_name}{output_dir}nearby_amenities.json"):
    amenities_dict = json.load(open(f"{dir_name}{output_dir}nearby_amenities.json"))

for token in tokens:    
    for category in category_ids:
        ## set x and y
        x = len(amenities_dict[category])
        y = len(amenities_dict[category])+500
        if y > len(property_data['Coordinates'].keys()):
            y = len(property_data['Coordinates'].keys())

        for index in range(x,y):
            amenities_dict = find_poi(property_data, index, token, buffer_size, category, amenities_dict)

## write json
for category in category_ids:
    property_data['Park'] = amenities_dict[280]
    property_data['PostOffice'] = amenities_dict[370]
    property_data['PTV'] = amenities_dict[604]

json.dump(property_data, open(f"{dir_name}{output_dir}nearby_amenities.json", 'w'))

# write csv
data = pd.read_json(f"{dir_name}{output_dir}neary_amenities.json")
data.to_csv(f"{dir_name}{output_dir}nearby_amenities.csv")

## manual input for routes that cannot be found
## issues from driveways longer that 350m and old roadworks in Rockbank
## 10497, 10498, 10561, 10581, 10590, 10591, 11129, 11728, 11729, 12047, 12797
