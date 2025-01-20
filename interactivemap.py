import folium
import json


# center around Amsterdam
m = folium.Map(location=[52.3676, 4.9041], zoom_start=13)


# load the geojson data
with open("./data/amsterdam_neighbourhoods.json") as f:
    geojson_data = json.load(f)


# with clickable map
folium.GeoJson(
    geojson_data,
    name="geojson",
    style_function=lambda x: {
        "fillColor": "green",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    },
    popup=folium.GeoJsonPopup(
        fields=["Buurt", "Wijk", "Oppervlakte_m2"],
        aliases=["Buurt:", "Wijk:", "Oppervlakte (m²):"],
        localize=True,
        labels=True,
        sticky=True,
    ),
).add_to(m)

# save the map in map folder
m.save("./maps/amsterdam_neighbourhoods_green.html")
