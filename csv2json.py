import csv     # imports the csv module
import sys      # imports the sys module
import json

stores = {}
custom_delimiter = ";";

f = open(sys.argv[1], 'rb') # opens the csv file
try:
        reader = csv.reader(f,delimiter=custom_delimiter)  # creates the reader object
        line_num = 0; # create base incremental
        for row in reader:   # iterates the rows of the file in orders
                if line_num == 0: # If first line, this is the header
                        header = {} # Create json for header
                        header_count = 0 # create base incremental
                        # Add header columns to json for later use
                        for word in row:
                                header[header_count] = word
                                header_count += 1
                else:
                        values = {}
                        value_count = 0
                        storecount = len(stores)
                        stores[storecount] = {}
                        for word in row:
                                stores[storecount][header[value_count]] = word
                                value_count += 1
                line_num += 1
finally:
        f.close()      # closing csv file

print json.dumps(stores)
