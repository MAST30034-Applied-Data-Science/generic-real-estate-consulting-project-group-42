"""
Records the number of schools within a 30 min drive and the distance to the closest primary and secondary school
"""

# Import necessary libraries
import json
import os
import pandas as pd
import time

from dotenv import load_dotenv
from helper_functions import get_closest, get_route
from shapely.geometry import Point, Polygon
from openrouteservice import client, isochrones

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/curated/"

# Load tokens and set variables
load_dotenv()
num_tokens = 34
tokens = []
for i in range(1,num_tokens+1):
    token = os.environ.get(f"token_{i}")
    tokens.append(token)
nearby_properties = {}

# Read data
property_data = json.load(open( f"{dir_name}{relative_dir}properties_processed.json" ))
school_data = pd.read_csv(f"{dir_name}{relative_dir}schools/school_info.csv")
filtered_schools = school_data[(school_data["School_Type"] == "Primary")|\
    (school_data["School_Type"] =="Pri/Sec")|(school_data["School_Type"] == "Secondary")]

# For each school find the properties in 30 min driving distance
school_isos = {}
for i in range(0,num_tokens):
    token = tokens[i]
    schools = filtered_schools.iloc[i*500:i*500+500] # take 500 at a time for API limit
    for index, row in schools.iterrows():
        school_coords = [row["Longitude"], row["Latitude"]]
        school_key = f"{row['School_Type']}, {school_coords}"

        ors = client.Client(key=token)

        # Find search region
        params_iso = {"locations": [school_coords],
                    "profile": "driving-car",
                    "range":[1800] # 30 mins
                    }

        iso = ors.isochrones(**params_iso)["features"][0]["geometry"]
        school_isos[school_key] = Polygon(iso["coordinates"][0])
        time.sleep(0.5)

# For each property, list all schools that it is within 30min from
nearby_schools = {}
for property in property_data["Coordinates"].keys():
    nearby_schools[property] = []
    backwards = list(map(float,property_data["Coordinates"][property][1:-1].split(",")))
    coords = Point(backwards[1], backwards[0])
    for school in school_isos.keys():
        if coords.within(school_isos[school]):
            nearby_schools[property].append(school)

# Count number of schools
school_count = {}
for property in nearby_schools.keys():
    school_count[property] = len(nearby_schools[property])

# Find nearest schools
school_dist = {}
school_dist["Primary"]={}
school_dist["Secondary"]={}
manual_input = [10497, 10561, 10581, 10590, 10591, 11129, 11728, 12057, 12797]
for i in range(0,num_tokens):
    token = tokens[i]
    x = len(school_dist["Primary"])
    y = x + 666 # API max 2000/calls per loop 3

    if y > len(nearby_schools.keys()):
        y = len(nearby_schools.keys())

    for property in range(x,y):
        if property in manual_input:
            school_dist["Primary"][str(property)] = 0
            school_dist["Secondary"][str(property)] = 0
        else: 
            schools = nearby_schools[str(property)]
            values = []
            for school in schools:
                split = list(school.split(", "))
                values.append((split[0], list(map(float,[split[1][1:],split[2][:-1]]))))
            backwards = list(map(float,property_data["Coordinates"][str(property)][1:-1].split(",")))
            prop_coords = [backwards[1], backwards[0]]
    
            # Separate school types
            pri_sec = [x[1] for x in values if x[0]=="Pri/Sec"]
            pri = [x[1] for x in values if x[0]=="Primary"]
            sec = [x[1] for x in values if x[0]=="Secondary"]

            # Find closest school
            pri_sec_school = get_closest(prop_coords,pri_sec)
            pri_school = get_closest(prop_coords,pri)
            sec_school = get_closest(prop_coords,sec)

            # Get route to closest school
            pri_sec_route = get_route(prop_coords,pri_sec_school, token)
            pri_route = get_route(prop_coords,pri_school, token)
            sec_route = get_route(prop_coords,sec_school, token)

            # Save information
            if (pri_sec_route["duration"] < pri_route["duration"]) & (pri_sec_route["duration"]!=0) | (pri_sec_route["duration"] > pri_route["duration"]) & (pri_route["duration"]==0):
                school_dist["Primary"][str(property)] = pri_sec_route
            else:
                school_dist["Primary"][str(property)] = pri_route

            if (pri_sec_route["duration"] < sec_route["duration"]) & (pri_sec_route["duration"]!=0) | (pri_sec_route["duration"] > sec_route["duration"]) & (sec_route["duration"]==0):
                school_dist["Secondary"][str(property)] = pri_sec_route
            else:
                school_dist["Secondary"][str(property)] = sec_route

# Manual input
school_dist["Primary"][str(10497)] = {'distance': 30400.0, 'duration': 1670.0}
school_dist["Secondary"][str(10497)] = {'distance': 0.0, 'duration': 0.0}
school_dist["Primary"][str(10561)] = {'distance': 1300.0, 'duration': 204.0}
school_dist["Secondary"][str(10561)] = {'distance': 11300.0, 'duration': 623.0}
school_dist["Primary"][str(10581)] = {'distance': 1300.0, 'duration': 204.0}
school_dist["Secondary"][str(10581)] = {'distance': 8800.0, 'duration': 698.0}
school_dist["Primary"][str(10590)] =  {'distance': 1300.0, 'duration': 204.0}
school_dist["Secondary"][str(10590)] = {'distance': 8800.0, 'duration': 698.0}
school_dist["Primary"][str(10591)] = {'distance': 1300.0, 'duration': 204.0}
school_dist["Secondary"][str(10591)] = {'distance': 8800.0, 'duration': 698.0}
school_dist["Primary"][str(11129)] = {'distance': 16200.0, 'duration': 1448.0}
school_dist["Secondary"][str(11129)] = {'distance': 21100.0, 'duration': 1511.0}
school_dist["Primary"][str(11728)] = {'distance': 9600.0, 'duration': 755.0}
school_dist["Secondary"][str(11728)] = {'distance': 9400.0, 'duration': 736.0}
school_dist["Primary"][str(12057)] = {'distance': 10.0, 'duration': 30.0}
school_dist["Secondary"][str(12057)] = {'distance': 10.0, 'duration': 30.0}
school_dist["Primary"][str(12797)] = {'distance': 3800.0, 'duration': 268.0}
school_dist["Secondary"][str(12797)] = {'distance': 3100.0, 'duration': 194.0}

# Save info
property_data["Nearby_Schools"] = school_count
property_data["Primary_Distance"] = school_dist["Primary"]
property_data["Secondary_Distance"] = school_dist["Secondary"]

# Write json
json.dump(property_data, open(f"{dir_name}{relative_dir}school_distances.json", "w"))

# Write csv
data = pd.read_json(f"{dir_name}{relative_dir}school_distances.json")
data.to_csv(f"{dir_name}{relative_dir}school_distances.csv")

print("Completed finding distance to closest schools")