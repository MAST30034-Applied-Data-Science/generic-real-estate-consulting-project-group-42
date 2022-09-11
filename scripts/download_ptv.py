"""
Counts PTV stops within 1km from each property
"""

import geopandas
import json
import os

from dotenv import load_dotenv
from openrouteservice import client, places

## find directory
dir_name = os.path.dirname(__file__)
output_dir = '../data/curated/'

## set variables
load_dotenv()
tokens = []
for i in range(1,17): 
    token = os.environ[f'token_{i}']
    tokens.append(token)
category_ids = [587, 588, 604, 607]
buffer_size = 2000   # between 1-2000


if not os.isfile(f'{dir_name}{output_dir}num_ptv.json'):
    x = 1
    y = 501
else:
    data = json.load(open( f"{dir_name}{output_dir}num_ptv.json" ))
    x = len(data) + 1
    y = len(data) + 501


## read apartment data
property_data = json.load(open( f"{dir_name}{output_dir}property_metadata.json" ))

for token in tokens:
    for index in range(x,y):
        if index > len(property_data.keys()):
            break
        key = list(property_data.keys())[index]
        coords = property_data[key]['Coordinates']

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
            property_data[key]['PTV'] = distances[0:3]
        else:
            property_data[key]['PTV'] = distances

    ## write new file
    if not os.path.exists(f'{dir_name}{output_dir}num_ptv.json'):
        json.dump(property_data, open(f"{dir_name}{output_dir}num_ptv.json", 'w'))
    else: 
        data.append(property_data)
        json.dump(data, open(f"{dir_name}{output_dir}num_ptv.json", 'w'))