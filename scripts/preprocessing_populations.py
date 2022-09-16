import os
import pandas as pd

# takes a census dataframe as input and returns a clean version
def clean_census_df(df, year):
    df_selected = df.iloc[1:, [0, 3]].rename(columns={0: 'postcode', 3: f'population_{year}'})
    df_selected['postcode'] = df_selected['postcode'].str.replace(r'POA', '')
    return df_selected

dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = '/data/raw/external/'
relative_dir_curated = '/data/curated/'

# data input
population_2011 = pd.read_csv(dir_name + relative_dir_raw + '2011_census.csv', header=None, index_col=False)
population_2016 = pd.read_csv(dir_name + relative_dir_raw + '2016_census.csv', header=None, index_col=False)
population_2021 = pd.read_csv(dir_name + relative_dir_raw + '2021_census.csv', header=None, index_col=False)

# clean dataframes
population_2011_clean = clean_census_df(population_2011, '2011')
population_2016_clean = clean_census_df(population_2016, '2016')
population_2021_clean = clean_census_df(population_2021, '2021')

# merge and save
population_history_df = population_2011_clean.merge(population_2016_clean, on='postcode').merge(population_2021_clean, on='postcode')
population_history_df.to_csv(dir_name + relative_dir_curated + 'population_history.csv', index=False)