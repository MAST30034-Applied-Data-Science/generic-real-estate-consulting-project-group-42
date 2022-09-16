
import os
import pandas as pd

dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = '/data/raw/external/'
relative_dir_curated = '/data/curated/'

postcode = pd.read_csv(dir_name + relative_dir_raw + 'postcode.csv', header=None)
unique_postcode = postcode.iloc[:,0].drop_duplicates()
unique_postcode.to_csv(dir_name + relative_dir_curated + 'unique_postcodes.csv', index=False, header=False)

mapping = pd.read_excel(dir_name + relative_dir_raw + "1270055006_CG_POSTCODE_2011_SA2_2011.xlsx", sheet_name='Table 5', header=[6])
print(mapping.head())