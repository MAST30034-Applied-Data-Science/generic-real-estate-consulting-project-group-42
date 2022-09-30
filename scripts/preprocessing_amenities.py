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
## cbd distance
10497 # cbd {'distance': 295100.0, 'duration': 13050.05}
10561 # cbd {'distance': 36300.0, 'duration': 2070.0}, park {'distance': 1200.0, 'duration': 240.0}, train {'distance': 1300.0, 'duration': 180.0}
10581 # cbd {'distance': 36200.0, 'duration': 2016.0}, park {'distance': 1000.0, 'duration': 240.0}, train {'distance': 1100.0, 'duration': 120.0}
10590 # cbd {'distance': 36250.0, 'duration': 2010.0}, park {'distance': 800.0, 'duration': 180.0}, train {'distance': 900.0, 'duration': 120.0}
10591 # cbd {'distance': 36300.0, 'duration': 2070.0}, park {'distance': 1200.0, 'duration': 240.0}, train {'distance': 1300.0, 'duration': 180.0}
11129 # cbd {'distance': 320900.0, 'duration': 14124.0}
11728 # cbd {'distance': 226000.0, 'duration': 9336.0}
11729 # cbd {'distance': 201400.0, 'duration': 8430}
12047 # park {'distance': 3200.0, 'duration': 360.0}
12715 # park {'distance': 1300.0, 'duration': 180.0}
12717 # park {'distance': 1300.0, 'duration': 180.0}
12797 # cbd {'distance': 82700.0, 'duration': 66.3}, park {'distance': 1600.0, 'duration': 180.0}
