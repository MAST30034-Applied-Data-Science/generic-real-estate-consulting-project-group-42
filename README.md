# Generic Real Estate Consulting Project
Group Number: 42
Group Name: Meaning of Life
Team Members: Winona Freihaut (1084858), Jade Devlin (1168815), Jia Williams Murnane (1168850), Raphaella Bichler (1168860), Kelman Chen (1168867)
Tutorial: Wednesday 11am Calvin Huang

Research Goal:
To determine the appropriate level fo rent a real estate company should be listing their properties, and which properties are most likely to increase in the next five years. Questions to answer:
    - What are the most important internal and external features in predicting rental prices?
    - What are the top 10 suburbs with the highest predicted growth rate?
    - What are the most livable and affordable suburbs according to you chosen metrics?

## Instructions:
From scripts folder:
1. Run `download_external.py`
2. Run `preprocessing_postcodes.py`
3. Run `scrape.ipynb` (hypothetically)
4. Run `preprocessing_income.py`
5. Run `preprocessing_properties.ipynb`
6. Run `preprocessing_school.py` (hypothetically)
7. Run `preprocessing_amenities.py` (hypothetically)

## order (informal)
1. download_external.py - all external data downloaded
2. preprocessing_postcodes.py - clean postcodes for scraping property data
3. scrape.ipynb - download property data (will need to be a script later?)
4. preprocessing_properties.ipynb - cleaning property data returning prepropcessed_properties.json/.csv
5. preprocessing (cleaning) external datasets - income, schools
6. ors related scripts - preprocessing amenities, cbd_distance
7. merge ors datasets
8. modelling/forecasting