import os
print("Current working directory at: " + os.getcwd())

print("Fetching raw hospitalization data for London from directory: ")
print("data/raw/london-hospitalizations-from-excel.csv")

# from line 15
london_hos_data = open("data/raw/london-hospitalizations-from-excel.csv", "r").readlines()[15].split(',')
formatted_london_hos_data = open("data/formatted/london-hospitalizations.csv", "w+")

for char in range(2, len(london_hos_data)):

    formatted_london_hos_data.writelines([london_hos_data[char] + '\n'])

print("Raw hospitalization data has been formatted.")
print("The formatted hospitalization data can be found at `data/formatted/london-hospitalizations`")
