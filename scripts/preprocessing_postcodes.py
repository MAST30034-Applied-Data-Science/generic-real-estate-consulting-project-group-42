
import pandas as pd

# read in postcode csv 
relative_dir = "../data/raw/external/"

# to run, working directory needs to be set to /scripts
postcode = pd.read_csv(relative_dir + 'postcode.csv', header=None)
unique_postcode = postcode.iloc[:,0].drop_duplicates()
unique_postcode.to_csv("../data/curated/unique_postcodes.csv", index=False, header=False)