"""
Selects relevant columns of the census data
"""

# Importing necessary libraries
import os
import pandas as pd

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = "/data/raw/external/"
relative_dir_curated = "/data/curated/"

census_pop = pd.read_csv(dir_name + relative_dir_raw + "2021Census_T01_VIC_SA2.csv", index_col=False)
census_finance = pd.read_csv(dir_name + relative_dir_raw + "2021Census_T02_VIC_SA2.csv", index_col=False)

census_pop_filtered = census_pop[["SA2_CODE_2021", "Tot_persons_C11_P", "Tot_persons_C16_P", "Tot_persons_C21_P"]]
census_finance_filtered = census_finance.drop(["Med_age_persns_C2011", "Med_age_persns_C2016", "Med_age_persns_C2021", 
                                                "Med_Famly_inc_we_C2011", "Med_Famly_inc_we_C2016", "Med_Famly_inc_we_C2021", 
                                                "Avg_num_p_per_brm_C2011", "Avg_num_p_per_brm_C2016", "Avg_num_p_per_brm_C2021"],
                                                axis=1)
census_df = census_pop_filtered.merge(census_finance_filtered, on="SA2_CODE_2021")
census_df = census_df.rename(columns={"SA2_CODE_2021": "sa2_2021"})

# Save data
census_df.to_csv(dir_name + relative_dir_curated + "census_data.csv", index=False)

print("Completed preprocessing census data")