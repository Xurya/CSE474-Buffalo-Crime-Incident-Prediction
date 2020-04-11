import csv
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import statsmodels.formula.api as stats

current_file_count = 0
# validation_file_iter = 0
colnames = ["incident_id", "case_number", "incident_datetime", "incident_type_primary", "incident_description",
            "clearance_type", "address_1", "address_2", "city", "state", "zip", "country", "latitude", "longitude",
            "created_at", "updated_at", "location", "hour_of_day", "day_of_week", "parent_incident_type",
            "Council Districts", "Police Districts", "Zip Codes", "Tracts", "Block Groups", "Blocks"]


def main():
    # Take the files and sort them by date to create new sorted csvs
    with open("Crime_Incidents.csv") as f:
        next(f)
        reader = csv.reader(f)
        sort = sorted(reader, key=lambda row: sort_by_date(row[2]))

    # Writes to a single, sorted file. Previously tested and now commented out for reference
    #   generate_crime_incident_sort(sort)

    partitions = list(partition(sort, 100))
    partition_writer(partitions)

    model_generator()


def visualize(data_frame, surface1, surface2, surface3):
    # https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(data_frame['Longitude'], data_frame['Latitude'], data_frame['Date'], c='red', marker='o', alpha=0.5)
    ax.plot_surface(surface1, surface2, surface3.reshape(surface1.shape), color='b', alpha=0.3)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Date')
    plt.show()


# Writes multiple csv files by partitioning the sorted crime incidents by date
def partition_writer(partitions):
    file_count = 0
    for lst in partitions:
        with open("Crime_Incidents_Sorted" + str(file_count) + ".csv", 'w', newline='') as f:
            writer = csv.writer(f)
            for line in lst:
                writer.writerow(line)
        file_count += 1


# Writes to a single, sorted file. Previously tested and now commented out for reference
def generate_crime_incident_sort(sort):
    with open("Crime_Incidents_Sorted.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for line in sort:
            writer.writerow(line)


# handler for model generation
def model_generator():
    # obtain current file
    data = pd.read_csv("Crime_Incidents_Sorted" + str(current_file_count) + ".csv", names=colnames)
    lat = data.latitude.tolist()
    long = data.longitude.tolist()
    pos = list(zip(lat, long))
    date = list(map(lambda x: time_convert(sort_by_date(x)), data.incident_datetime.tolist()))
    print(date)

    regression(pos, date)


def generate_graph(data_frame, input):
    surfacex, surfacey = np.meshgrid(np.linspace(data_frame.Longitude.min(), data_frame.Longitude.max(), 100),
                                     np.linspace(data_frame.Latitude.min(), data_frame.Latitude.max(), 100))
    temp_frame = pd.DataFrame({'Longitude': surfacex.ravel(), 'Latitude': surfacey.ravel()})
    post = np.array(input.predict(exog=temp_frame))
    return surfacex, surfacey, post


def time_convert(dt):
    return 10000 * dt.year + 100 * dt.month + dt.day


def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def sort_by_date(date):
    if date == "":
        return datetime.now()
    return datetime.strptime(date, "%m/%d/%Y %I:%M:%S %p")


def regression(pos, date):
    data_frame = pd.DataFrame(pos, columns=['Longitude', 'Latitude'])
    data_frame['Date'] = pd.Series(date)

    model = stats.ols(formula='Date ~ Longitude + Latitude', data=data_frame)
    preprocessed = model.fit()

    surfacex, surfacey, processed = generate_graph(data_frame, preprocessed)

    visualize(data_frame, surfacex, surfacey, processed)


if __name__ == "__main__":
    main()
