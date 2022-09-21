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

if not os.path.exists(dir_name + relative_dir + 'external/' + 'population'):
    os.makedirs(dir_name + relative_dir + 'external/' + 'population')
    print('Created population directory')

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
urls = [
    "https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2014-15-2018-19/6524055002_DO002.xlsx", 
    "https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2014-15-2018-19/6524055002_DO001.xlsx"]

filenames = ["income_distribution.xlsx", "income_history.xlsx"]
for i in range(0, len(urls)):
    url = urls[i]
    filename = filenames[i]
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
pop_base_url = 'https://www.abs.gov.au/census/find-census-data/datapacks/download/'
pop_filenames = ['2021_GCP_POA_for_VIC_short-header', '2016_GCP_POA_for_VIC_short-header', '2011_BCP_POA_for_VIC_short-header']
pop_csv_dirs = ['/2021 Census GCP Postal Areas for VIC/2021Census_G01_VIC_POA.csv', 
                '/2016 Census GCP Postal Areas for VIC/2016Census_G01_VIC_POA.csv',
                '/2011 Census BCP Postal Areas for VIC/VIC/2011Census_B01_VIC_POA_short.csv']
pop_years = ['2021', '2016', '2011']

for filename, csv_dir, pop_year in zip(pop_filenames, pop_csv_dirs, pop_years):
    output_dir = dir_name + relative_dir + 'population/'

    urlretrieve(f'{pop_base_url}{filename}.zip', f'{output_dir}{filename}.zip')

    # extract zip file
    with zipfile.ZipFile(f'{output_dir}{filename}.zip', "r") as zip_ref:
        zip_ref.extractall(f'{output_dir}{filename}')

    os.rename(f'{output_dir}{filename}{csv_dir}', dir_name + relative_dir + f'{pop_year}_census.csv')

    print(f"Completed downloading and extracting {pop_year}_census.csv")

