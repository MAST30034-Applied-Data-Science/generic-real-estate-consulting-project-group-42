import os
import pandas as pd
from helper_functions import preprocess_mapping


dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir_raw = '/data/raw/external/'
relative_dir_curated = '/data/curated/'


# read in and preprocess all required dataframes
sa2_postcode_mapping_2011 = preprocess_mapping(dir_name + relative_dir_raw + "1270055006_CG_POSTCODE_2011_SA2_2011.xls",
                                                'POSTCODE', 'SA2_MAINCODE_2011', 'postcode_2011', 'sa2_2011')

sa2_2011_to_2016 = preprocess_mapping(dir_name + relative_dir_raw + 'sa2_2011_to_2016/' + 'CG_SA2_2011_SA2_2016.xls',
                                        'SA2_MAINCODE_2016', 'SA2_MAINCODE_2011', 'sa2_2016', 'sa2_2011')   

sa2_2016_to_2021 = preprocess_mapping(dir_name + relative_dir_raw + 'sa2_2016_to_2021.csv', 
                                            'SA2_MAINCODE_2016', 'SA2_CODE_2021', 'sa2_2016', 'sa2_2021')  

postcode_2011_to_2016 = preprocess_mapping(dir_name + relative_dir_raw + 'postcode_2011_to_2016/' + 'CG_POA_2011_POA_2016.xls',
                                            'POA_CODE_2011', 'POA_CODE_2016', 'postcode_2011', 'postcode_2016')  

postcode_2016_to_2021 = preprocess_mapping(dir_name + relative_dir_raw + 'postcode_2016_to_2021.csv', 
                                            'POA_CODE_2016', 'POA_CODE_2021', 'postcode_2016', 'postcode_2021') 

# merge dataframes to create 2021 mapping
sa2_postcode_mapping_2021 = sa2_2016_to_2021.merge(sa2_2011_to_2016, on='sa2_2016').merge(sa2_postcode_mapping_2011, on='sa2_2011')\
                                            .merge(postcode_2011_to_2016, on='postcode_2011').merge(postcode_2016_to_2021, on='postcode_2016')
sa2_postcode_mapping_2021 = sa2_postcode_mapping_2021[['sa2_2021', 'postcode_2021']].drop_duplicates()

# output csv
sa2_postcode_mapping_2021.to_csv(dir_name + relative_dir_curated + 'sa2_postcode_mapping_2021.csv', index=False)