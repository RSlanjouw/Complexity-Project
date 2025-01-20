#download the file from the url
import requests

URL = ""


def download_file(url, filename="amsterdam.geojson"):
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)

download_file(URL)

