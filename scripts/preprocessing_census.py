import os
import pandas as pd


dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = '/data/raw/external/'
relative_dir_curated = '/data/curated/'

census_pop = pd.read_csv(dir_name + relative_dir_raw + '2021Census_T01_VIC_SA2.csv', index_col=False)
census_finance = pd.read_csv(dir_name + relative_dir_raw + '2021Census_T02_VIC_SA2.csv', index_col=False)

census_pop_filtered = census_pop[['SA2_CODE_2021', 'Tot_persons_C11_P', 'Tot_persons_C16_P', 'Tot_persons_C21_P']]
census_df = census_pop_filtered.merge(census_finance, on='SA2_CODE_2021')

census_df.to_csv(dir_name + relative_dir_curated + 'census_data.csv', index=False)