import os
print("Current working directory at: " + os.getcwd())

print("Fetching raw hospitalization data for New York from directory: ")
print("data/raw/ny-hospitalizations.csv")

ny_hos_data = open("data/raw/ny-hospitalizations.csv", "r").readlines()
formatted_ny_hos_data = open("studies/formatted/ny-hospitalizations.csv", "w+")

for line in range(1, len(ny_hos_data)):

    formatted_ny_hos_data.writelines([ny_hos_data[line].split(',')[2] + '\n'])

print("Raw hospitalization data has been formatted.")
print("The formatted hospitalization data can be found at `data/formatted/ny-hospitalizations`")
