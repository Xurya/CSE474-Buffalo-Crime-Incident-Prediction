import csv
import operator
from datetime import datetime


def main():
    # Take the files and sort them by date to create new sorted csvs
    with open("Crime_Incidents.csv") as f:
        next(f)
        reader = csv.reader(f)
        sort = sorted(reader, key=lambda row: sort_by_date(row[2]))

    # Writes to a single, sorted file. Previously tested and now commented out for reference
    # with open("Crime_Incidents_Sorted.csv", 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     for line in sort:
    #         writer.writerow(line)

    partitions = list(partition(sort, 100))
    fileCount = 0;
    for lst in partitions:
        with open("Crime_Incidents_Sorted" + str(fileCount) + ".csv", 'w', newline='') as f:
            writer = csv.writer(f)
            for line in lst:
                writer.writerow(line)
        fileCount += 1


def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def sort_by_date(date):
    if date == '':
        return datetime.now()
    return datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")


if __name__ == "__main__":
    main()
