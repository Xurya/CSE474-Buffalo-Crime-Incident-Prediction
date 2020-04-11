import csv
import operator
from datetime import datetime

def main():
    #Take the files and sort them by date to create new sorted csvs
    with open("Crime_Incidents.csv") as f:
        reader = csv.reader(f)
        sort = sorted(reader, key=lambda row: datetime.strptime(row[2], "%m/%d/%y %H:%M:%S %p"))
        for line in sort:
            print(line)

if __name__ == "__main__":
    main()
