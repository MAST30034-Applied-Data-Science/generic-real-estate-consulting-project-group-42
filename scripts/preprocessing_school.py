"""
Script for preprocessing school dataset
"""
import pandas as pd
import os

# Setting up directory and defining filename
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/raw/external/"
fn = dir_name + relative_dir + "schools.csv"

# Read in csv file containing school dataset into Pandas dataframe
schools_df = pd.read_csv(fn, encoding = "ISO-8859-1")
#print(schools_df)

# Defining desired attributes
COLUMNS = ["School_Name", "Education_Sector", "School_Type", "Address_Postcode", "X", "Y"]

# Extracting only desired attributes from dataframe
schools_df = schools_df[COLUMNS]
#print(schools_df.columns)

# Renaming column headers 
schools_df = schools_df.rename(columns = {"Address_Postcode": "Postcode", "Y": "Latitude", "X": "Longitude"})

# Filtering for NaN values
for col in schools_df.columns:
    if not schools_df[schools_df[col].isna()].empty:
        print(f"{col} contains NaN values")

# Finding instances with NaN latitude or longitude
print(schools_df[schools_df["Latitude"].isna()])
print(schools_df[schools_df["Longitude"].isna()])

# Manually adding the coordinates for St Ignatius College Geelong 
LAT = -38.1893
LONG = 144.5582
schools_df.loc[schools_df["School_Name"] == "St Ignatius College Geelong", "Latitude"] = LAT
schools_df.loc[schools_df["School_Name"] == "St Ignatius College Geelong", "Longitude"] = LONG
#print(schools_df[schools_df["School_Name"] == "St Ignatius College Geelong"])

# Create new directory in curated data folder
relative_dir = "../data/curated/"
target_dir = "schools"
if not os.path.exists(f"{dir_name}{relative_dir}{target_dir}"):
    os.makedirs(f"{dir_name}{relative_dir}{target_dir}")

# Save preprocessed dataframe under schools in curated data folder
schools_df.to_csv(dir_name + "../data/curated/schools/school_info.csv", index = False)


# Calculating the number of Government, Independent and Catholic schools of each school type in each postcode
agg_df = schools_df.groupby(by = ["Postcode", "Education_Sector", "School_Type"], as_index = False).count()
agg_df["Number_of_Schools"] = agg_df["School_Name"]
agg_df = agg_df.drop(columns = ["School_Name", "Longitude", "Latitude"])
#print(agg_df)

# Saving aggregated dataframe under schools in curated data folder
agg_df.to_csv(dir_name + "../data/curated/schools/school_counts.csv")