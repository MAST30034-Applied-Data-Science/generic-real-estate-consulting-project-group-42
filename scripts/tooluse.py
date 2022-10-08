# libraries to inport
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from scipy.spatial import distance
import json 
import os

# user input for postcode 
postcode_input = input ("Enter a postcode: ")
postcode = int(postcode_input)

print ("The postcode you entered is: ", postcode)

## find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = '/data/curated/'


database = pd.read_csv(f'{dir_name}{relative_dir}growthrate_afford_live.csv')
with open(f"{dir_name}{relative_dir}postcode_dists.json", 'r') as file:
    closest_postcodes = json.load(file)

try:
    top_ten = closest_postcodes.get(str(postcode))
    top_ten_postcodes = list(top_ten.keys())
except: 
    print(f"{postcode} is not available")
    quit()


output = pd.DataFrame(columns=['Unnamed: 0', 'Postcode', 'Growth Rate', 'Standardised Affordability', 'Standardised Liveability'])
for i in range(0, len(top_ten)):

    data = database.loc[(database['Postcode'] == int(top_ten_postcodes[i]))]
    if data.empty:
        print(f"No data for {top_ten_postcodes[i]}")
    else:
        #output = output.append(pd.Series(poo, index = output.columns[:len(poo)]), ignore_index = True)
        print(data)
# function to search up closest postcodes and details 
