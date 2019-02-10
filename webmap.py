import pandas as pd
import folium
import geocoder
import os
import webbrowser


def read_data(title, filename):
    data = pd.read_csv(filename, error_bad_lines=False)
    data.dropna()
    data_input = data[data["movie"].str.contains(title)]

    data_locations = []

    for loc, mov in zip(data_input["location"], data_input["movie"]):
        g = geocoder.arcgis(loc)
        lat_lng = g.latlng
        lat_lng.append(mov)
        data_locations.append(lat_lng)

    return data_locations


def create_map(data_locations):
    web_map = folium.Map(location=[0, 0], zoom_start=2)

    fg_location = folium.FeatureGroup(name="Film Locations")
    for lt, ln, movie_title in data_locations:
        fg_location.add_child(folium.Marker(location=[lt, ln],
                                            popup=movie_title,
                                            icon=folium.Icon(color="green",
                                                             icon="film")))

    fg_population = folium.FeatureGroup(name="Population")
    fg_population.add_child(folium.GeoJson(
        data=open('world.json', 'r', encoding='utf-8-sig').read(),
        style_function=lambda x: {
            'fillColor': 'green'if x['properties']['POP2005'] < 10**7
            else 'orange' if 10**7 <= x['properties']['POP2005'] < 2*10**7
            else 'red'}))

    web_map.add_child(fg_location)
    web_map.add_child(fg_population)
    web_map.add_child(folium.LayerControl())
    web_map.save("map.html")
    webbrowser.open('file://' + os.path.realpath("map.html"))


if __name__ == "__main__":
    title = input("Enter any title you want to find: ")
    data_locations = read_data(title, "locations.csv")
    create_map(data_locations)
