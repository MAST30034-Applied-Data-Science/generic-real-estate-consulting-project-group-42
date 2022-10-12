"""
Scrapes Domain.com.au for properties for rent in Victoria
"""
# Importing necessary libraries
import os
import pandas as pd
import random
import requests
import re
import timeit
import time

from bs4 import BeautifulSoup
from collections import defaultdict
from helper_functions import progress_tracker
from IPython.display import clear_output 

# Find directory
dir_name = os.path.dirname(__file__)
dir_name = os.path.dirname(dir_name)
relative_dir = "/data/"

# Define constants
BASE_URL = "https://www.domain.com.au"
N_PAGES = range(1, 11) 
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

postcodes = pd.read_csv(f"{dir_name}{relative_dir}curated/unique_postcodes.csv", header=None).squeeze()

url_dict = defaultdict(dict)
property_metadata = defaultdict(dict)

# Define progress tracker
start = timeit.default_timer()

# Index & enumerate are for progress tracking, can be removed for final submission
for index, postcode in enumerate(postcodes):
    clear_output(wait=True) # for progress tracking

    url_links = []
    
    # Generate list of urls to visit
    for page in N_PAGES:
        url = BASE_URL + f"/rent/?postcode={postcode}&page={page}" 
        bs_object = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser") 
        time.sleep(random.randint(0, 3))

        # Find the unordered list (ul) elements which are the results, then
        index_links = bs_object.find("ul", {"data-testid": "results"}) 

        # If there are no links, break
        if (index_links == None):
            break 

        # Find all href (a) tags that are from the base_url website.
        index_links = index_links.findAll("a",href=re.compile(f"{BASE_URL}/*"))
            
        for link in index_links:
            # If its a property address, add it to the list
            if "address" in link["class"]:
                url_links.append(link["href"])

    url_dict[postcode] = url_links

    # For progress tracking
    curr_progress = index/len(postcodes)
    stop = timeit.default_timer()
    progress_tracker(start, stop, curr_progress)

# for progress tracking
start = timeit.default_timer() 
property_metadata = defaultdict(dict)


# For each url, scrape features
# Index & enumerate are for progress tracking, can be removed for final submission
for index, postcode in enumerate(url_dict):
    clear_output(wait=True) # for progress tracking

    url_links = url_dict.get(postcode)

    for property_url in url_links:
        bs_object = BeautifulSoup(requests.get(property_url, headers=headers).text, "html.parser")
        time.sleep(0.5)

        # Looks for the header class to get property name
        name = bs_object.find("h1", {"class": "css-164r41r"})
        if name == None: 
            break 
        else: 
            property_metadata[property_url]["Name"] = name.text

        # Regex to find the cost in the summary title 
        cost_finder = re.compile(r'[0-9]+.?[0-9]+') # this regex search assumes that the first numeric value is the cost per week 
        cost_text = bs_object \
            .find("div", {"data-testid": "listing-details__summary-title"}) \
            .text

        # Extracts the cost from the summary title and adds to dictionary. 
        cost = cost_finder.search(cost_text)
        if cost == None: 
            property_metadata[property_url]["Cost"] = 0
        else:
            property_metadata[property_url]["Cost"] = cost.group()
            
        # Extract coordinates from the hyperlink provided
        # Finds latitude and longitude from integrated Google Map
        property_metadata[property_url]["Coordinates"] = [
            float(coord) for coord in re.findall(
                r'destination=([-\s,\d\.]+)', 
                bs_object \
                    .find(
                        "a",
                        {"target": "_blank", "rel": "noopener noreferer"}
                    ) \
                    .attrs["href"]
            )[0].split(",")
        ]
        
        # Extracts # of bedrooms, # of baths and # of parking spots 
        rooms_info = bs_object.find("div", {"data-testid": "property-features"}).findAll("span", {"data-testid": "property-features-text-container"})
        for i in range(0, min(3, len(rooms_info))):
            attr_desc = str(rooms_info[i].text).split(" ")

            property_metadata[property_url][attr_desc[1]] = attr_desc[0]

        # Extracts property type from the site 
        property_metadata[property_url]["Property_Type"] = bs_object \
            .find("div", {"data-testid": "listing-summary-property-type"}).find("span", {"class" : "css-in3yi3"}).text

        # Extract real estate agency
        agency = bs_object.find("a", {"data-testid" : "listing-details__agent-details-agent-company-name"})
        if agency == None:
            property_metadata[property_url]["Agency"] = "-"
        else:
            property_metadata[property_url]["Agency"] = agency.text

        property_metadata[property_url]["Postcode"] = postcode

    # for progress tracking
    curr_progress = index/len(url_dict)
    stop = timeit.default_timer()
    progress_tracker(start, stop, curr_progress)

data = []

for url in url_dict.values():
    for url_link in url:
        info = property_metadata.get(url_link)
        if info == None:
            break
        else:
            data.append(list(info.values()))        
        
      
property_df = pd.DataFrame(data)

property_df = property_df.iloc[:,]
property_df.columns = ["Name", "Cost", "Coordinates", "Bed", "Bath", "Parking", "Property_Type", "Agency", "Postcode"]

property_df.to_csv(f"{dir_name}{relative_dir}raw/property_data.csv")  

print("Completed scraping property data")