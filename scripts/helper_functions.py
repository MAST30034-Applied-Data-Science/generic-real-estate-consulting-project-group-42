"""
A collection of all script functions and repeated notebook functions
"""

import geopy.distance
import numpy as np
import pandas as pd
import time
import timeit

from openrouteservice import client, directions, places

def convert_census_to_postcode(census_df, sa2_postcode_map, agg_function="mean_no_zero"):
    """
    Inputs census data as indexed by SA2 and converts it to postcode through aggregation
    """

    if agg_function == "mean_no_zero":
        agg_func = lambda lst: round(np.mean([x for x in lst if x > 0]), 2)


    census_df_postcode = sa2_postcode_map.merge(census_df, on="sa2_2021").drop("sa2_2021", axis=1)
    census_df_postcode = census_df_postcode[census_df_postcode["postcode_2021"] >= 3000]

    census_df_postcode_agg = census_df_postcode.groupby("postcode_2021").agg(
        tot_population_11 = pd.NamedAgg(column="Tot_persons_C11_P", aggfunc=sum),
        tot_population_16 = pd.NamedAgg(column="Tot_persons_C16_P", aggfunc=sum),
        tot_population_21 = pd.NamedAgg(column="Tot_persons_C21_P", aggfunc=sum),
        avg_med_mortg_rep_11 = pd.NamedAgg(column="Med_mortg_rep_mon_C2011", aggfunc=agg_func),
        avg_med_mortg_rep_16 = pd.NamedAgg(column="Med_mortg_rep_mon_C2016", aggfunc=agg_func),
        avg_med_mortg_rep_21 = pd.NamedAgg(column="Med_mortg_rep_mon_C2021", aggfunc=agg_func),
        avg_med_person_inc_11 = pd.NamedAgg(column="Med_person_inc_we_C2011", aggfunc=agg_func),
        avg_med_person_inc_16 = pd.NamedAgg(column="Med_person_inc_we_C2016", aggfunc=agg_func),
        avg_med_person_inc_21 = pd.NamedAgg(column="Med_person_inc_we_C2021", aggfunc=agg_func),
        avg_med_rent_16 = pd.NamedAgg(column="Med_rent_weekly_C2011", aggfunc=agg_func),
        avg_med_rent_11 = pd.NamedAgg(column="Med_rent_weekly_C2016", aggfunc=agg_func),
        avg_med_rent_21 = pd.NamedAgg(column="Med_rent_weekly_C2021", aggfunc=agg_func),
        avg_med_hh_inc_16 = pd.NamedAgg(column="Med_tot_hh_inc_wee_C2011", aggfunc=agg_func),
        avg_med_hh_inc_11 = pd.NamedAgg(column="Med_tot_hh_inc_wee_C2016", aggfunc=agg_func),
        avg_med_hh_inc_21 = pd.NamedAgg(column="Med_tot_hh_inc_wee_C2021", aggfunc=agg_func),
        tot_avg_hh_size_16 = pd.NamedAgg(column="Average_hh_size_C2011", aggfunc=agg_func),
        tot_avg_hh_size_11 = pd.NamedAgg(column="Average_hh_size_C2016", aggfunc=agg_func),
        tot_avg_hh_size_21 = pd.NamedAgg(column="Average_hh_size_C2021", aggfunc=agg_func),
    ).reset_index()

    return census_df_postcode_agg

def get_closest(property, pois):
    """
    Finds the closest point of interest in a list of coordinates
    """
    prop_coords = (property[1],property[0])
    if len(pois) == 0: # for if no nearby points of interest
        return 0
    
    distances = []
    for poi in pois:
        distances.append(geopy.distance.geodesic(prop_coords, (poi[1],poi[0])))
    
    return pois[distances.index(min(distances))]

def get_route(start, end, token):
    """
    Finds the route between two points
    """
    if end == 0:
        return {"distance": 0.0, "duration": 0.0}
    
    coords = [tuple(start), tuple(end)]
    ors = client.Client(key=token)
    request = {"coordinates": coords,
            "profile": "driving-car",
            "geometry": "true",
            "format_out":"geojson"}
    route = ors.directions(**request)
    time.sleep(0.5)
    return route["features"][0]["properties"]["summary"]

def find_poi(property_data, index, token, buffer_size, category, amenities_dict):
    """
    Pings ORS to find points of interest
    """
    backwards = list(map(float,property_data["Coordinates"][str(index)][1:-1].split(",")))
    coords = [backwards[1], backwards[0]]
    ors = client.Client(key=token)

    # Find poi
    query = {"request": "pois",
            "geojson": {"type":"Point","coordinates":coords},
            "buffer": buffer_size,
            "filter_category_ids": category,
            "sortby":"distance",
            "limit": 2}

    features = ors.places(**query)["features"]
    destination = features[0]["geometry"]["coordinates"]

    # Find route
    info = get_route(coords, destination, token)

    # Add information
    amenities_dict[category][str(index)] = info
    time.sleep(0.5)

    return amenities_dict

def preprocess_mapping(input_dir, column1, column2, column1_renamed, column2_renamed):
    """
    Takes input directory, and column names as input, reads in the input directory according to the fyle type before
    pre-processsing and returning preprocessed dataframe 
    """
    if input_dir[-3:] == "csv":
        df = pd.read_csv(input_dir)
    elif input_dir[-3:] == "xls":
        df = pd.read_excel(input_dir, sheet_name="Table 3", header=[5], engine="xlrd")

    # Remove NaN values 
    df = df[~df[column1].isna()]
    df = df[~df[column2].isna()]

    # Select necessary rows and columns
    df = df[:-1]
    df = df[[column1, column2]]

    # Convert to string type
    df[column1] = df[column1].astype(int).astype(str)
    df[column2] = df[column2].astype(int).astype(str)

    df = df.rename(columns={column1: column1_renamed, column2: column2_renamed})

    return df

def separate_dictionary(data, column):
    """
    Separates a dictionary into each key
    """
    return pd.concat(
        [data.drop(column, axis=1), 
        data[column].map(eval).apply(pd.Series)]
    , axis=1)

def progress_tracker(start, stop, curr_progress):
    """
    Determines how long an operation will take
    """
    if (curr_progress*100) < 5:
        expected_time = "Calculating..."
    else:
        time_perc = timeit.default_timer()
        expected_time = np.round(((time_perc-start) / curr_progress)/60, 2)

    print("Current progress:", np.round(curr_progress*100, 2), "%")
    print("current run time:", np.round((stop-start)/60, 2), "minutes")
    print("Expected run time:", expected_time, "minutes")
