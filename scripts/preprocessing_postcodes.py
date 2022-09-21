
import os
import pandas as pd

dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = '/data/raw/external/'
relative_dir_curated = '/data/curated/'

# postcode list
postcode = pd.read_csv(dir_name + relative_dir_raw + 'postcode.csv', header=None)
unique_postcode = postcode.iloc[:,0].drop_duplicates()
unique_postcode.to_csv(dir_name + relative_dir_curated + 'unique_postcodes.csv', index=False, header=False)

# postcode to sa2 mapping
mapping = pd.read_excel(dir_name + relative_dir_raw + "1270055006_CG_POSTCODE_2011_SA2_2011.xls", sheet_name='Table 3', header=[5], engine="xlrd")
mapping = mapping[~mapping['POSTCODE'].isna()]

idx = mapping.groupby(['POSTCODE'])['RATIO'].transform(max) == mapping['RATIO']
mapping = mapping[idx]
mapping = mapping.drop(['POSTCODE.1', 'PERCENTAGE', 'RATIO'], axis=1)
mapping.to_csv(dir_name + relative_dir_raw + 'sa2_postcode_map.csv')