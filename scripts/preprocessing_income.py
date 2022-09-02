"""
Summary
"""

from pyspark.sql import SparkSession
import pandas as pd
import geopandas as gpd
import os

# # Create a spark session (which will run spark jobs)
# spark = (
#     SparkSession.builder.appName("MAST30034 Project 1")
#     .config("spark.sql.repl.eagerEval.enabled", True) 
#     .config("spark.sql.parquet.cacheMetadata", "true")
#     .config("spark.executor.memory", "2g")
#     .config("spark.driver.memory", "4g")
#     .getOrCreate()
# )


# read in SA2 data
dir_name = os.path.dirname(__file__)
relative_dir = "/../data/raw/external/"
# SA2 = spark.read.csv(dir_name + '/../data/raw/external/SA2_2016_AUST.csv')
SA2 = pd.read_csv(dir_name + relative_dir + 'SA2_2016_AUST.csv')
sf = gpd.read_file(dir_name + relative_dir + 'SA2_shapefile/SA2_2016_AUST.shp')
gdf = gpd.GeoDataFrame(
    pd.merge(SA2, sf, left_on='SA2_MAINCODE_2016', right_on='SA2_MAIN16', how='inner')
)

geoJSON = gdf[['LocationID', 'geometry']].drop('SA2_MAIN16', axis=1).to_json()
gdf.head()

# read in income data
income = pd.read_excel(dir_name + relative_dir + "income_distribution.xlsx", sheet_name='Table 2.4', header=[5,6])
income.rename(columns={'Unnamed: 0_level_0':'SA2', 'Unnamed: 1_level_0':'SA2_name'}, inplace = True)
income.columns = income.columns.droplevel(-1)

# select only victorian data
vic_index = income.index[income['SA2'] == 'Victoria'].values[0]
qld_index = income.index[income['SA2'] == 'Queensland'].values[0]

vic_income = income.iloc[vic_index+1:qld_index]
vic_income = vic_income.merge(SA2, how='left', left_on='SA2', right_on='SA2_MAINCODE_2016').drop(['SA2_MAINCODE_2016', 'STATE_CODE_2016', 'STATE_NAME_2016'], axis=1)

print(vic_income.head())
print(sf.head())