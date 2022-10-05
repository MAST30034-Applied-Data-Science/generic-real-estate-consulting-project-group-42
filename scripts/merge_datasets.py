"""
Merging datasets on required 
"""

import os
import pandas as pd


## find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = '/data/curated/'

amenities = pd.read_csv(f'{dir_name}{relative_dir}nearby_amenities.csv')
school = pd.read_csv(f'{dir_name}{relative_dir}school_distances.csv')