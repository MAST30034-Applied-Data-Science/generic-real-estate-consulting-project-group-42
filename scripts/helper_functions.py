import geopy.distance
import numpy as np
import pandas as pd
import time

from openrouteservice import client, directions, places

def convert_census_to_postcode(census_df, sa2_postcode_map, agg_function='mean_no_zero'):
    ''' Inputs census data as indexed by SA2 and converts it to postcode through aggregation
    '''

    if agg_function == 'mean_no_zero':
        agg_func = lambda lst: round(np.mean([x for x in lst if x > 0]), 2)


    census_df_postcode = sa2_postcode_map.merge(census_df, on='sa2_2021').drop('sa2_2021', axis=1)
    census_df_postcode = census_df_postcode[census_df_postcode['postcode_2021'] >= 3000]

    census_df_postcode_agg = census_df_postcode.groupby('postcode_2021').agg(
        tot_population_11 = pd.NamedAgg(column='Tot_persons_C11_P', aggfunc=sum),
        tot_population_16 = pd.NamedAgg(column='Tot_persons_C16_P', aggfunc=sum),
        tot_population_21 = pd.NamedAgg(column='Tot_persons_C21_P', aggfunc=sum),
        avg_med_mortg_rep_11 = pd.NamedAgg(column='Med_mortg_rep_mon_C2011', aggfunc=agg_func),
        avg_med_mortg_rep_16 = pd.NamedAgg(column='Med_mortg_rep_mon_C2016', aggfunc=agg_func),
        avg_med_mortg_rep_21 = pd.NamedAgg(column='Med_mortg_rep_mon_C2021', aggfunc=agg_func),
        avg_med_person_inc_11 = pd.NamedAgg(column='Med_person_inc_we_C2011', aggfunc=agg_func),
        avg_med_person_inc_16 = pd.NamedAgg(column='Med_person_inc_we_C2016', aggfunc=agg_func),
        avg_med_person_inc_21 = pd.NamedAgg(column='Med_person_inc_we_C2021', aggfunc=agg_func),
        avg_med_rent_16 = pd.NamedAgg(column='Med_rent_weekly_C2011', aggfunc=agg_func),
        avg_med_rent_11 = pd.NamedAgg(column='Med_rent_weekly_C2016', aggfunc=agg_func),
        avg_med_rent_21 = pd.NamedAgg(column='Med_rent_weekly_C2021', aggfunc=agg_func),
        avg_med_hh_inc_16 = pd.NamedAgg(column='Med_tot_hh_inc_wee_C2011', aggfunc=agg_func),
        avg_med_hh_inc_11 = pd.NamedAgg(column='Med_tot_hh_inc_wee_C2016', aggfunc=agg_func),
        avg_med_hh_inc_21 = pd.NamedAgg(column='Med_tot_hh_inc_wee_C2021', aggfunc=agg_func),
        tot_avg_hh_size_16 = pd.NamedAgg(column='Average_hh_size_C2011', aggfunc=agg_func),
        tot_avg_hh_size_11 = pd.NamedAgg(column='Average_hh_size_C2016', aggfunc=agg_func),
        tot_avg_hh_size_21 = pd.NamedAgg(column='Average_hh_size_C2021', aggfunc=agg_func),
    ).reset_index()

    return census_df_postcode_agg

def get_closest(property, schools):
    '''find the schools with the closest distance'''
    prop_coords = (property[1],property[0])
    if len(schools) == 0: ## for if no nearby schools
        return 0
    
    distances = []
    for school in schools:
        distances.append(geopy.distance.geodesic(prop_coords, (school[1],school[0])))
    
    return schools[distances.index(min(distances))]

def get_route(start, end, token):
    '''find the route'''
    if end == 0:
        return {'distance': 0.0, 'duration': 0.0}
    
    coords = [tuple(start), tuple(end)]
    ors = client.Client(key=token)
    request = {'coordinates': coords,
            'profile': 'driving-car',
            'geometry': 'true',
            'format_out':'geojson'}
    route = ors.directions(**request)
    time.sleep(0.5)
    return route['features'][0]['properties']['summary']

def find_poi(property_data, index, token, buffer_size, category, amenities_dict):
    '''
    Pings ORS to find points of interest
    '''
    backwards = list(map(float,property_data['Coordinates'][str(index)][1:-1].split(',')))
    coords = [backwards[1], backwards[0]]
    ors = client.Client(key=token)

    ## find poi
    query = {'request': 'pois',
            'geojson': {'type':'Point','coordinates':coords},
            'buffer': buffer_size,
            'filter_category_ids': category,
            'sortby':'distance',
            'limit': 2}

    features = ors.places(**query)['features']
    destination = features[0]['geometry']['coordinates']

    ## find route
    info = get_route(coords, destination, token)

    ## add information
    amenities_dict[category][str(index)] = info
    time.sleep(0.5)

    return amenities_dict
