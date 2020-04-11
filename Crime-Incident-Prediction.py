import csv
import operator
from datetime import datetime


def main():
    # Take the files and sort them by date to create new sorted csvs
    with open("Crime_Incidents.csv") as f:
        next(f)
        reader = csv.reader(f)
        sort = sorted(reader, key=lambda row: sort_by_date(row[2]))

    with open("Crime_Incidents_Sorted.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for line in sort:
            writer.writerow(line)


def sort_by_date(date):
    if date == '':
        return datetime.now()
    return datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")


if __name__ == "__main__":
    main()
