"""
Downloads and saves external datasets.
"""

import os, requests, zipfile
from io import BytesIO
from urllib.request import urlretrieve

dir_name = os.path.dirname(__file__)
relative_dir = '../data/raw/external/'

for target_dir in ('domain', 'external'):
    if not os.path.exists(f'{dir_name}/{relative_dir}{target_dir}'):
        os.makedirs(f'{dir_name}/{relative_dir}{target_dir}')

#SA2 CSV file
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_csv.zip&1270.0.55.001&Data%20Cubes&9F6E4EB4E23B269FCA257FED0013A4F8&0&July%202016&12.07.2016&Latest"

filename = "SA2.csv"
output_dir = f"{dir_name}/{relative_dir}{filename}"

urlretrieve(url, output_dir)

# SA2 shapefile data
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&A09309ACB3FA50B8CA257FED0013D420&0&July%202016&12.07.2016&Latest"

req = requests.get(url)
filename = "SA2_shapefile"
output_dir = f"{dir_name}/{relative_dir}{filename}"

with open(filename,'wb') as output_file:
    output_file.write(req.content)

SA_zipfile = zipfile.ZipFile(BytesIO(req.content))
SA_zipfile.extractall(output_dir)

## Areas of Victoria Shapefiles

# Local Government Area (match SAL 2021)
url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/LGA_2021_AUST_GDA2020_SHP.zip"

req = requests.get(url)
filename = "LGA_shapefile"
output_dir = f"{dir_name}/{relative_dir}{filename}"

with open(filename,'wb') as output_file:
    output_file.write(req.content)

LGA_zipfile = zipfile.ZipFile(BytesIO(req.content))
LGA_zipfile.extractall(output_dir)

# Suburbs and Localities (newest edition 2021)
url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SAL_2021_AUST_GDA2020_SHP.zip"

req = requests.get(url)
filename = "SAL_shapefile"
output_dir = f"{dir_name}/{relative_dir}{filename}"

with open(filename,'wb') as output_file:
    output_file.write(req.content)

SAL_zipfile = zipfile.ZipFile(BytesIO(req.content))
SAL_zipfile.extractall(output_dir)