"""
Tool to rank the 10 nearest postcodes on desireability metrics
"""

# Importing necessary libraries
import json 
import pandas as pd
import os
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = '/data/curated/'

# User input for postcode 
postcode_input = input ("Enter a postcode: ")
postcode = int(postcode_input)

print ("The postcode you entered is: ", postcode)

# Find nearest postcodes
database = pd.read_csv(f'{dir_name}{relative_dir}growthrate_afford_live.csv')
with open(f"{dir_name}{relative_dir}postcode_dists.json", 'r') as file:
    closest_postcodes = json.load(file)

try:
    top_ten = closest_postcodes.get(str(postcode))
    top_ten_postcodes = list(top_ten.keys())
except: 
    print(f"{postcode} is not available")
    quit()

# Print information
initial_pc_data = database.loc[(database['Postcode'] == int(postcode))]
initial_pc_data = initial_pc_data.drop(columns='Unnamed: 0')

output = pd.DataFrame(columns=['Unnamed: 0', 'Postcode', 'Growth Rate', 'Standardised Affordability', 'Standardised Liveability'])
for i in range(0, len(top_ten)):

    data = database.loc[(database['Postcode'] == int(top_ten_postcodes[i]))]
    if data.empty:
        print(f"No data for {top_ten_postcodes[i]}")
    else:
        output = output.append(data, ignore_index = True)

output = output.drop(columns='Unnamed: 0')
output[f'Distance from {postcode}'] = top_ten.values()

print("\n")
print("Here is the data for your current postcode: ")
print(initial_pc_data)
print("\n")
print("Here are is the data for the surrounding postcodes: ")
print(output)
