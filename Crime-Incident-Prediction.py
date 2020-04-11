import csv

def main():
    #Take the files and sort them by date to create new sorted csvs
    with open("Crime_Incidents.csv") as f:
        reader = csv.reader(f)


if __name__ == "__main__":
    main()
