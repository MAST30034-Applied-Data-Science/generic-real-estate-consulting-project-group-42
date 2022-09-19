"""
Downloads and saves external datasets.
"""

import os, requests, zipfile
from io import BytesIO
from urllib.request import urlretrieve

## find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = '/data/raw/'

## create separate folders for data
if not os.path.exists(dir_name + relative_dir + 'external'):
    os.makedirs(dir_name + relative_dir + 'external')
    print('Created external directory')

relative_dir = '/data/raw/external/'

## DOWNLOAD SA2 DATA
# SA2 csv file
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_csv.zip&1270.0.55.001&Data%20Cubes&9F6E4EB4E23B269FCA257FED0013A4F8&0&July%202016&12.07.2016&Latest"

output_dir = f"{dir_name}{relative_dir}"

req = requests.get(url)
with zipfile.ZipFile(BytesIO(req.content)) as sa2_zipfile:
    sa2_zipfile.extractall(output_dir)

print('Completed downloading and extracting SA2 csv data')

# SA2 shapefile
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&A09309ACB3FA50B8CA257FED0013D420&0&July%202016&12.07.2016&Latest"

req = requests.get(url)
filename = "SA2_shapefile"
output_dir = f"{dir_name}{relative_dir}{filename}"

SA_zipfile = zipfile.ZipFile(BytesIO(req.content))
SA_zipfile.extractall(output_dir)

print('Completed downloading and extracting SA2 shapefile')

# INCOME DATA
url = "https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2014-15-2018-19/6524055002_DO002.xlsx"

filename = "income_distribution.xlsx"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

print('Completed downloading income data')

## SCHOOLS
url = "https://www.education.vic.gov.au/Documents/about/research/datavic/dv331_schoollocations2022.csv"

filename = "schools.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

print('Completed downloading schools data')

## POSTCODES
url = "https://zen10.com.au/wp-content/uploads/2011/07/Victoria-Postcodes.csv"

filename = "postcode.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

print('Completed downloading postcodes data')

## POSTCODE TO SA2 MAPPING
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055006_CG_POSTCODE_2011_SA2_2011.zip&1270.0.55.006&Data%20Cubes&70A3CE8A2E6F9A6BCA257A29001979B2&0&July%202011&27.06.2012&Latest"

filename = "mapping_postcode_SA2.xlsx"
output_dir = f"{dir_name}{relative_dir}"

req = requests.get(url)
with zipfile.ZipFile(BytesIO(req.content)) as sa2_zipfile:
    sa2_zipfile.extractall(output_dir)

print('Completed downloading and extracting postcodes to SA2 mapping data')

## POPULATIONS
pop_url = 'https://www.abs.gov.au/census/find-census-data/datapacks/download/2021_TSP_SA2_for_VIC_short-header.zip'
output_dir = dir_name + relative_dir
folder_name = 'SA2_VIC_Census_TSP'
pop_filenames = ['2021Census_T01_VIC_SA2.csv', '2021Census_T02_VIC_SA2.csv']
files_dir = 'SA2_VIC_Census_TSP/2021 Census TSP Statistical Area 2 for VIC/'

urlretrieve(pop_url, f'{output_dir}{folder_name}.zip')
with zipfile.ZipFile(f'{output_dir}{folder_name}.zip', "r") as zip_ref:
    zip_ref.extractall(f'{output_dir}{folder_name}')

for filename in pop_filenames:
    os.rename(f'{output_dir}{files_dir}{filename}', f'{output_dir}{filename}')

print(f"Completed downloading and extracting census data")

