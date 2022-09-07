
from pyspark.sql import SparkSession
import pandas as pd
import geopandas as gpd
import os

# read in postcode csv 
dir_name = os.path.dirname(__file__)
relative_dir = "../data/raw/external/"

postcode = pd.read_csv(dir_name + relative_dir + 'postcode.csv', header = None)
postcode = postcode.iloc[:,0].unique()
postcode.to_csv("../data/curated/unique_postcodes.csv")
