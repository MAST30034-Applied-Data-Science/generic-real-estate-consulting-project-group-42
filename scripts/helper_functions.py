import numpy as np
import pandas as pd

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