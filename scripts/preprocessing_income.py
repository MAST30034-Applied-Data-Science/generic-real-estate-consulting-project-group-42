"""
Summary
"""

import pandas as pd
import geopandas as gpd
import os
import folium

dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/raw/external/"

# read in SA2 data
SA2 = pd.read_csv(dir_name + relative_dir + 'SA2_2016_AUST.csv')
SA2 = SA2.rename(columns={'SA2_MAINCODE_2016':"SA2_MAIN16"})
SA2 = SA2[SA2['STATE_NAME_2016'] == 'Victoria']
SA2['SA2_MAIN16'] = SA2['SA2_MAIN16'].astype(str)

# read in shapefile and merge with SA2
sf = gpd.read_file(dir_name + relative_dir + 'SA2_shapefile/SA2_2016_AUST.shp')
gdf = gpd.GeoDataFrame(
    pd.merge(SA2, sf, on='SA2_MAIN16', how='inner').drop_duplicates()
)
geoJSON = gdf[['SA2_MAIN16', 'geometry']].to_json()

# read in income data
income = pd.read_excel(dir_name + relative_dir + "income_distribution.xlsx", sheet_name='Table 2.4', header=[5,6])
income.rename(columns={'Unnamed: 0_level_0':'SA2', 'Unnamed: 1_level_0':'SA2_name'}, inplace = True)
income.columns = income.columns.droplevel(-1)

# read in historical income data
history = pd.read_excel(dir_name + relative_dir + "income_history.xlsx", sheet_name='Table 1.4', header=[5,6])
history = history[['Earners (persons)', 'Median age of earners (years)', 'Sum ($)', 'Median ($)']]
print(history['Earners (persons)']['2014-15'].head())

# select only victorian data
vic_index = income.index[income['SA2'] == 'Victoria'].values[0]
qld_index = income.index[income['SA2'] == 'Queensland'].values[0]
vic_income = income.iloc[vic_index+1:qld_index]

# remove NaN values
vic_income = vic_income[vic_income['Sum'] != 'np']

# select column attributes for income data
vic_income = vic_income[['SA2', 'SA2_name', 'Earners', 'Median age of earners', 'Sum', 'Median']].rename(columns={'Median age of earners':'Median_age'})

# convert strings to integer values
vic_income['SA2'] = vic_income['SA2'].astype(str)

attributes = ['Sum', 'Median', 'Median_age']

# for attribute in attributes:
    
#     vic_income[attribute] = vic_income[attribute].astype(int)

#     m = folium.Map(location=[-37.84, 144.96], tiles="cartodbpositron", zoom_start=7)

#     # refer to the folium documentations on more information on how to plot aggregated data.
#     c = folium.Choropleth(
#         geo_data=geoJSON, # geoJSON 
#         name='choropleth', # name of plot
#         data=vic_income, # data source
#         columns=['SA2', attribute], # the columns required
#         key_on='properties.SA2_MAIN16', # this is from the geoJSON's properties
#         fill_color='BuPu', # color scheme
#         nan_fill_color='black',
#         legend_name=attribute
#     )

#     c.add_to(m)
#     m.save(dir_name + '/plots/'+ attribute + '_income.html')
#     m

# vic_income.to_csv(dir_name+relative_dir + 'vic_income.csv')