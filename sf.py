import os
print("Current working directory at: " + os.getcwd())

print("Fetching raw hospitalization data for San Francisco from directory: ")
print("data/raw/sf-hospitalizations.csv")

sf_hos_data = open("data/raw/sf-hospitalizations.csv", "r").readlines()
formatted_sf_hos_data = open("studies/formatted/sf-hospitalizations.csv", "w+")

for line in range(1, len(sf_hos_data)):

    formatted_sf_hos_data.writelines([sf_hos_data[line].split(',')[-1]])

print("Raw hospitalization data has been formatted.")
print("The formatted hospitalization data can be found at `data/formatted/sf-hospitalizations`")
