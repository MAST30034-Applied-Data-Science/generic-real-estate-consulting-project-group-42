import subprocess

subprocess.run("python3 download_external.py", shell=True)

subprocess.run("python3 preprocessing_postcodes.py", shell=True)

# subprocess.run("python3 download_property_data.py", shell=True)

subprocess.run("python3 preprocessing_properties.py", shell=True)

subprocess.run("python3 preprocessing_census.py", shell=True)

subprocess.run("python3 preprocessing_income.py", shell=True)

subprocess.run("python3  preprocessing_sa2_postcode_mapping.py", shell=True)

subprocess.run("python3 preprocessing_school.py", shell=True)

# subprocess.run("python3 preprocessing_distances.py", shell=True)

# subprocess.run("python3 preprocessing_school_distances.py", shell=True)

subprocess.run("python3 merge_datasets.py", shell=True)

subprocess.run("python3 featurise_distances.py", shell=True)