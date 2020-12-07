import os
print("Current working directory at: " + os.getcwd())

print("Fetching raw hospitalization data for Tokyo from directory: ")
print("data/raw/tokyo-hospitalizations-from-html-table.txt")

tokyo_hos_data = open("data/raw/tokyo-hospitalizations-from-html-table.txt", "r").readlines()
formatted_tokyo_hos_data = open("data/formatted/tokyo-hospitalizations.csv", "w+")

reversed_data_seq = []

for line in range(3, len(tokyo_hos_data)):

    # ignore all HTML code blocks unless on a line with a multiple of 4 (indexing starts at 0)
    if (line - 3) % 4 == 0:
        reversed_data_seq.append(tokyo_hos_data[line])

reversed_data_seq = reversed(reversed_data_seq)
formatted_tokyo_hos_data.writelines(reversed_data_seq)

print("Raw hospitalization data has been formatted.")
print("The formatted hospitalization data can be found at `data/formatted/tokyo-hospitalizations`")
