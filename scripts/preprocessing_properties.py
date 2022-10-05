"""
Cleans scraped property data
"""
import os
import pandas as pd


## find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = '/data/raw/'

## loads data
properties = pd.read_csv(f"{dir_name}{relative_dir}property_data.csv", index_col=0)

## reformat costs without commas
properties['Cost'] = properties['Cost'].str.replace(',', '')

## change null values to numeric zero
properties['Bed'] = properties['Bed'].replace('−', 0)
properties['Bath'] = properties['Bath'].replace('−', 1)
properties['Parking'] = properties['Parking'].replace('−', 0)

## Null postcodes and coordinates are invalid rows
properties = properties[~properties['Postcode'].isna()]
properties = properties[properties['Coordinates']!='[0.0, 0.0]']

## Convert column types
properties['Cost'] = properties['Cost'].astype(float)
properties['Bed'] = properties['Bed'].astype(int)
properties['Bath'] = properties['Bath'].astype(int)
properties['Parking'] = properties['Parking'].astype(int)
properties['Postcode'] = properties['Postcode'].astype(int).astype(str)

## Edit cost parameters properties
properties = properties[properties['Cost'] != 0]
properties = properties[properties['Cost'] <= 20000]

## Save data
new = properties.reset_index(drop=True)
new.to_csv('../data/curated/properties_processed.csv')
new.to_json('../data/curated/properties_processed.json')