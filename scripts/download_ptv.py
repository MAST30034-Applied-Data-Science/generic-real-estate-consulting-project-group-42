"""
Finds distance to nearest public transport
"""

import geopandas
import os

from openrouteservice import client, places

## find directory
dir_name = os.path.dirname(__file__)
output_dir = '../data/curated/'

## set variables
api_key = ''
category_ids = [587, 588, 604, 607]
buffer_size = 200   # between 1-2000

## read apartment data
coords = ''     # coords of apartment

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
    distances.append(poi['properties']['distance'])
