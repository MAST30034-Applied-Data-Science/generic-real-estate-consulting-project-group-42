"""
Downloads and saves external datasets.
"""

import os, requests, zipfile
from io import BytesIO
from urllib.request import urlretrieve

dir_name = os.path.dirname(__file__)
relative_dir = '../data/raw/'

for target_dir in ('domain', 'external'):
    if not os.path.exists(relative_dir + target_dir):
        os.makedirs(relative_dir + target_dir)

#SA2 CSV file
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_csv.zip&1270.0.55.001&Data%20Cubes&9F6E4EB4E23B269FCA257FED0013A4F8&0&July%202016&12.07.2016&Latest"

filename = "SA2.csv"
output_dir = f"{dir_name}/{relative_dir}external/{filename}"

urlretrieve(url, output_dir)

# SA2 shapefile data
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&A09309ACB3FA50B8CA257FED0013D420&0&July%202016&12.07.2016&Latest"

req = requests.get(url)
filename = "SA2_shapefile"
output_dir = f"{dir_name}/{relative_dir}external/{filename}"

with open(filename,'wb') as output_file:
    output_file.write(req.content)

zipfile = zipfile.ZipFile(BytesIO(req.content))
zipfile.extractall(output_dir)