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
for target_dir in (['external', 'domain']):
    if not os.path.exists(f'{dir_name}{relative_dir}{target_dir}'):
        os.makedirs(f'{dir_name}{relative_dir}{target_dir}')

relative_dir = '/data/raw/external/'

## DOWNLOAD SA2 DATA
# SA2 csv file
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_csv.zip&1270.0.55.001&Data%20Cubes&9F6E4EB4E23B269FCA257FED0013A4F8&0&July%202016&12.07.2016&Latest"

filename = "SA2_2016_AUST.csv"
output_dir = f"{dir_name}{relative_dir}"
print("Started")
req = requests.get(url)
  
with zipfile.ZipFile(BytesIO(req.content)) as sa2_zipfile:
    sa2_zipfile.extractall(output_dir)

# SA2 shapefile
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&A09309ACB3FA50B8CA257FED0013D420&0&July%202016&12.07.2016&Latest"

req = requests.get(url)
filename = "SA2_shapefile"
output_dir = f"{dir_name}{relative_dir}{filename}"

SA_zipfile = zipfile.ZipFile(BytesIO(req.content))
SA_zipfile.extractall(output_dir)

# INCOME DATA
url = "https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2014-15-2018-19/6524055002_DO002.xlsx"

filename = "income_distribution.xlsx"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

## SCHOOLS
url = "https://www.education.vic.gov.au/Documents/about/research/datavic/dv331_schoollocations2022.csv"

filename = "schools.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

## POSTCODES
url = "https://zen10.com.au/wp-content/uploads/2011/07/Victoria-Postcodes.csv"

filename = "postcode.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)