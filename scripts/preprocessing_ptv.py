"""
Records the distance of the 3 nearest PTV stops
"""

import json
import os
import pandas as pd

from dotenv import load_dotenv
from openrouteservice import client, places

## find directory
dir_name = os.path.dirname(__file__)
output_dir = '../data/curated/'

## set variables
load_dotenv()
tokens = []
for i in range(1,17): 
    token = os.environ.get(f'token_{i}')
    tokens.append(token)
category_ids = [587, 588, 604, 607]
buffer_size = 2000   # between 1-2000
ptv_dict = {}


## read apartment data
property_data = json.load(open( f"{dir_name}{output_dir}properties_processed.json" ))

for i in range(1,9): # 500 per day, 60 per minute
    for token in tokens:
        ## set x and y
        x = ((i-1)*960)+(tokens.index(token)*60)
        y = ((i-1)*960)+(tokens.index(token)*60)+60
    
        for index in range(x,y):
            if index > len(property_data['Coordinates'].keys()):
                break
            coords=list(map(float,property_data['Coordinates'][str(index)][1:-1].split(',')))

            ## query code
            ors = client.Client(key=token)
            query = {'request': 'pois',
                    'geojson': {'type':'Point','coordinates':coords},
                    'buffer': buffer_size,
                    'filter_category_ids': category_ids,
                    'sortby':'distance'}
            features = ors.places(**query)['features']

            ## distances - direct meters
            distances = []
            for poi in features:
                distances.append(poi['properties']['distance'])
        
            ## add information
            if len(distances)>3:
                ptv_dict[str(index)] = distances[0:3]
            else:
                ptv_dict[str(index)] = distances
            

## write json
property_data['PTV'] = ptv_dict
json.dump(property_data, open(f"{dir_name}{output_dir}num_ptv.json", 'w'))

# write csv
data = pd.read_json(f"{dir_name}{output_dir}num_ptv.json")
data.to_csv(f"{dir_name}{output_dir}num_ptv.csv")