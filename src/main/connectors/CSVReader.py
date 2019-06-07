import csv
import json

csvfile = open('file.csv', 'r')

reader = csv.DictReader(csvfile)
for row in reader:
    json.dump(row)
