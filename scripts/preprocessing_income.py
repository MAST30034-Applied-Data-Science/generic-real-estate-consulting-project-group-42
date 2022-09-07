"""
Summary
"""

from pyspark.sql import SparkSession
import pandas as pd
import geopandas as gpd
import os
import folium

# # Create a spark session (which will run spark jobs)
# spark = (
#     SparkSession.builder.appName("MAST30034 Project 1")
#     .config("spark.sql.repl.eagerEval.enabled", True) 
#     .config("spark.sql.parquet.cacheMetadata", "true")
#     .config("spark.executor.memory", "2g")
#     .config("spark.driver.memory", "4g")
#     .getOrCreate()
# )

dir_name = os.path.dirname(__file__)
relative_dir = "/../data/raw/external/"

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

# select only victorian data
vic_index = income.index[income['SA2'] == 'Victoria'].values[0]
qld_index = income.index[income['SA2'] == 'Queensland'].values[0]

vic_income = income.iloc[vic_index+1:qld_index]
vic_income = vic_income[vic_income['Sum'] != 'np']
vic_income['Sum'] = vic_income['Sum'].astype(int)

m = folium.Map(location=[-37.84, 144.96], tiles="cartodbpositron", zoom_start=2)

# refer to the folium documentations on more information on how to plot aggregated data.
c = folium.Choropleth(
    geo_data=geoJSON, # geoJSON 
    name='choropleth', # name of plot
    data=vic_income, # data source
    columns=['SA2', 'Sum'], # the columns required
    key_on='properties.SA2_MAIN16', # this is from the geoJSON's properties
    fill_color='BuPu', # color scheme
    nan_fill_color='black',
    legend_name='Income Data'
)

c.add_to(m)

m.save(dir_name + '../plots/income.html')
m