
import pandas as pd

# read in postcode csv 
relative_dir = "../data/raw/external/"

postcode = pd.read_csv(relative_dir + 'postcode.csv', header=None)
unique_postcode = postcode.iloc[:,0].drop_duplicates()
unique_postcode.to_csv("../data/curated/unique_postcodes.csv", index=False, header=False)