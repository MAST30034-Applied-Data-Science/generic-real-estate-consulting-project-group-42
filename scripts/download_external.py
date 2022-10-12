"""
Downloads and saves external datasets.
"""

# Importing necessary libraries
import os, requests, zipfile
from io import BytesIO
from urllib.request import urlretrieve

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/raw/"

# Create separate folders for data
if not os.path.exists(f"{dir_name}{relative_dir}external"):
    os.makedirs(f"{dir_name}{relative_dir}external")
    print("Created external directory")
relative_dir = "/data/raw/external/"

# DOWNLOAD SA2 DATA
# SA2 csv file
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_csv.zip&1270.0.55.001&Data%20Cubes&9F6E4EB4E23B269FCA257FED0013A4F8&0&July%202016&12.07.2016&Latest"
output_dir = f"{dir_name}{relative_dir}"
req = requests.get(url)
with zipfile.ZipFile(BytesIO(req.content)) as sa2_zipfile:
    sa2_zipfile.extractall(output_dir)

print("Completed downloading and extracting SA2 csv data")

# SA2 shapefile
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&A09309ACB3FA50B8CA257FED0013D420&0&July%202016&12.07.2016&Latest"
req = requests.get(url)
filename = "SA2_shapefile"
output_dir = f"{dir_name}{relative_dir}{filename}"
SA_zipfile = zipfile.ZipFile(BytesIO(req.content))
SA_zipfile.extractall(output_dir)

print("Completed downloading and extracting SA2 shapefile")

## SCHOOLS
url = "https://www.education.vic.gov.au/Documents/about/research/datavic/dv331_schoollocations2022.csv"
filename = "schools.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

print("Completed downloading schools data")

## POSTCODES
url = "https://zen10.com.au/wp-content/uploads/2011/07/Victoria-Postcodes.csv"
filename = "postcode.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

url = "https://www.matthewproctor.com/Content/postcodes/australian_postcodes.zip"
filename = "australian_postcodes"
output_dir = f"{dir_name}{relative_dir}{filename}"
req = requests.get(url)
with zipfile.ZipFile(BytesIO(req.content)) as aus_postcode_zip:
    aus_postcode_zip.extractall(output_dir)

print("Completed downloading and extracting postcodes data")

## POSTCODE TO SA2 MAPPING 2011
url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055006_CG_POSTCODE_2011_SA2_2011.zip&1270.0.55.006&Data%20Cubes&70A3CE8A2E6F9A6BCA257A29001979B2&0&July%202011&27.06.2012&Latest"

filename = "mapping_postcode_SA2.xlsx"
output_dir = f"{dir_name}{relative_dir}"
req = requests.get(url)
with zipfile.ZipFile(BytesIO(req.content)) as mapping_postcode:
    mapping_postcode.extractall(output_dir)

print("Completed downloading and extracting postcodes to SA2 mapping data 2011")

## SA2 HISTORICAL CORRESPONDENCES
url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/correspondences/CG_SA2_2016_SA2_2021.csv"
filename = "sa2_2016_to_2021.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)


url = "https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&cg_sa2_2011_sa2_2016.zip&1270.0.55.001&Data%20Cubes&C9CFBB94B52B200DCA257FED0014C198&0&July%202016&12.07.2016&Latest"
filename = "sa2_2011_to_2016"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, f"{output_dir}.zip")
with zipfile.ZipFile(f"{output_dir}.zip", "r") as zip_ref:
    zip_ref.extractall(output_dir)

print("Completed downloading and extracting SA2 historical correspondences data")

## POSTCODE HISTORICAL CORRESPONDENCES
url = "https://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&cg_poa_2011_poa_2016.zip&1270.0.55.003&Data%20Cubes&3399EB98D8341DFFCA25802C0014C3D3&0&July%202016&13.09.2016&Previous"

filename = "postcode_2011_to_2016"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, f"{output_dir}.zip")
with zipfile.ZipFile(f"{output_dir}.zip", "r") as zip_ref:
    zip_ref.extractall(output_dir)


url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/correspondences/CG_POA_2016_POA_2021.csv"
filename = "postcode_2016_to_2021.csv"
output_dir = f"{dir_name}{relative_dir}{filename}"
urlretrieve(url, output_dir)

print("Completed downloading and extracting postcode historical correspondences data")

## POPULATIONS
pop_url = "https://www.abs.gov.au/census/find-census-data/datapacks/download/2021_TSP_SA2_for_VIC_short-header.zip"
output_dir = f"{dir_name}{relative_dir}"
folder_name = "SA2_VIC_Census_TSP"
pop_filenames = ["2021Census_T01_VIC_SA2.csv", "2021Census_T02_VIC_SA2.csv"]
files_dir = "SA2_VIC_Census_TSP/2021 Census TSP Statistical Area 2 for VIC/"

urlretrieve(pop_url, f"{output_dir}{folder_name}.zip")
with zipfile.ZipFile(f"{output_dir}{folder_name}.zip", "r") as zip_ref:
    zip_ref.extractall(f"{output_dir}{folder_name}")

for filename in pop_filenames:
    os.rename(f"{output_dir}{files_dir}{filename}", f"{output_dir}{filename}")

print("Completed downloading and extracting census data")

## POST CODE AREAS
url = "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/POA_2021_AUST_GDA2020_SHP.zip"
filename = "POA_2021_AUST_GDA2020"
output_dir = f"{dir_name}{relative_dir}{filename}"
req = requests.get(url)
with zipfile.ZipFile(BytesIO(req.content)) as poa_zipfile:
    poa_zipfile.extractall(f"{output_dir}POA_2021_AUST_GDA2020")

print("Completed downloading and extracting postal area data")

print("Completed downloading all files")