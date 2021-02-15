"""
Filter location.list file.
"""
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from haversine import haversine


def read_file() -> list:
    """
    Read locations.list file
    """
    datalist = []

    with open("locations.list", mode="r") as data:

        for line in data.readlines():
            try:
                linelist = line.strip("\n").split("\t")

                idx = linelist[0].find("(")
                year = int(linelist[0][idx+1:idx+5])

                idx = linelist[0][1:].find('"')
                name = linelist[0][1:idx+1]

                location = linelist[-1]

                mod_list = [year, name, location]
                datalist.append(mod_list)

            except (TypeError, ValueError):
                continue

    return datalist


def find_coords(user_year: int, user_coords: tuple) -> list:
    """
    Return a list of lists (max 10 sublists) filtered by distance.
    Return [[name, (lat, lon)], ...]
    """
    datalist = read_file()
    coords_list = []
    geolocator = Nominatim(user_agent="film_map")

    for data in datalist:

        if data[0] == user_year:

            try:
                location = geolocator.geocode(data[-1])
                coords = (location.latitude, location.longitude)
                data.append(coords)

                distance = haversine(user_coords, coords)
                data.append(distance)

                coords_list.append(data)

            except (AttributeError, OSError):
                continue

    coords_list.sort(key=lambda x: x[-1])

    ten_coords_list = [[elem[1], elem[3]] for elem in coords_list[:10]]

    return ten_coords_list


def user_input() -> tuple:
    """
    Get user input from terminal.
    Return (year, [lat, lon]).
    """
    try:
        year = int(
            input("Please enter a year you would like to have a map for: "))
        coords_str = input("Please enter your location(format: lat, long): ")

        coords = [float(coord) for coord in coords_str.split(",")]
        print("Map is generating...\nPlease wait...")

    except TypeError:
        return "Wrong input!"

    return year, coords


if __name__ == "__main__":
    print(find_coords(2016, (52.4081812, -1.510477)))
