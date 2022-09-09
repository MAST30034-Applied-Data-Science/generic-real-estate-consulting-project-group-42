"""
Counts PTV stops within 1km from each property
"""

import geopandas
import json
import os

from openrouteservice import client, places

## find directory
dir_name = os.path.dirname(__file__)
output_dir = '../data/curated/'

## set variables
api_key = ''
category_ids = [587, 588, 604, 607]
buffer_size = 2000   # between 1-2000
x = 1
y = 2

## read apartment data
property_data = json.load(open( f"{dir_name}{output_dir}property_metadata.json" ))

for index in range(x,y):
    coords = property_data[list(property_data.keys())[index]]['Coordinates']

    ## query code
    ors = client.Client(key=api_key)
    query = {'request': 'pois',
            'geojson': {'type':'Point','coordinates':coords},
            'buffer': buffer_size,
            'filter_category_ids': category_ids,
            'sortby':'distance'}
    features = ors.places(**query)['features']

    ## distances - direct meters
    distances = []
    for poi in features:
        if poi['properties']['distance']<1000:
            distances.append(poi['properties']['distance'])

    ## add information
    property_data[property]['PTV'] = len(distances)

## write new file
json.dump(property_data, open(f"{dir_name}{output_dir}ptv_{x}_{y}.json", 'w'))