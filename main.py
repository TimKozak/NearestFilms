"""
Main module of a program.
"""
import folium
from tools import find_coords, user_input


def creating_map():
    """
    Creates HTML page for a given data.
    """
    year, coords = user_input()
    locations = find_coords(year, coords)

    mp = folium.Map(location=coords, zoom_start=10)

    mp.add_child(folium.Marker(
        location=coords,
        popup="You are here",
        icon=folium.Icon(color='red',
                         icon_color='lightgray',
                         icon='home')))

    for location in locations:
        mp.add_child(folium.Marker(
            location=[location[1][0], location[1][1]],
            popup=location[0],
            icon=folium.Icon(color='green',
                             icon_color='white',
                             icon='cloud')))

        folium.PolyLine(locations=[(coords[0], coords[1]),
                                   location[1]], color='orange').add_to(mp)
    mp.save('nearest_films.html')
    print("Map succesfully generated")


if __name__ == "__main__":
    creating_map()
    # print(find_coords(2017, (52.4081812, -1.510477)))
