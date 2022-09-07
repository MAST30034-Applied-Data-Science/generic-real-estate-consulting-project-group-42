"""
Script for preprocessing school dataset
"""
import pandas as pd
import os

# Setting up directory
dir_name = os.path.dirname(__file__)
relative_dir = "../data/raw/external/"

# Read in csv file containing school dataset into Pandas dataframe
school_df = pd.read_csv(dir_name + relative_dir + "schools.csv")
school_df.head()