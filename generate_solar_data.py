import pycristoforo as pyc
import numpy as np
import json
import requests
import pandas as pd
import webbrowser
import folium
# from IPython.display import display

# Generate random coordinates around target country
def generate_coordinates(country="Netherlands", num_points=5):
    country_shape = pyc.get_shape(country)
    points = pyc.geoloc_generation(country_shape, num_points, country)
    # Code produces coordinates the wrong way round which must be rectified
    coordinates_wrong = [point['geometry']['coordinates'] for point in points]
    for c in coordinates_wrong:
        c[0], c[1] = c[1], c[0]
    return coordinates_wrong

def plot_points(coordinates):
    """
    Plot all the coordinates of the randomized points on a map
    """
    map = folium.Map(location=coordinates[0], zoom_start=12)
    for coordinate in coordinates:
        folium.Marker(coordinate).add_to(map)
    map.save("map.html")
    webbrowser.open("map.html")

def download_solar_data(api_key, coordinates, time_start = '2018-01-01', time_end = '2019-01-01'):
    """
    Download solar data for a particular set of coordinates [lat, long]
    """
    s = requests.session()
    api_base = 'https://www.renewables.ninja/api/'
    s.headers = {'Authorization': 'Token ' + api_key}
    url = api_base + 'data/pv'
    args = {
    'lat': coordinates[0],
    'lon': coordinates[1],
    'date_from': time_start,
    'date_to': time_end,
    'dataset': 'merra2',
    'capacity': 1.0,
    'system_loss': 0.1,
    'tracking': 2,
    'tilt': 35,
    'azim': 180,
    'format': 'json'
    }

    r = s.get(url, params=args)
    parsed_response = json.loads(r.text)
    data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
    data.to_csv('.\pvdata\pvdata_{:.3f}_{:.3f}.csv'.format(coordinates[0], coordinates[1]))

def main(api_key, num_points, seed):
    """
    Download solar data between 2018 and 2019 
    api_key - yur relevant api key for renewable ninja
    num points - number of points you would like to get data for within Netherlands
    seed - numpy random seed, ensure this is different from others in the group
    """
    np.random.seed(seed)
    coord_list = generate_coordinates(country="Netherlands", num_points=num_points) 
    plot_points(coord_list)
    for coordinates in coord_list:
        download_solar_data(api_key, coordinates)

if __name__ == '__main__':
    api_key = '38ad00aaa981b7910dc4a479672c3f9a0fa24efe'
    coordinates = [[52.4085, 6.6146]]
    for coords in coordinates:
        download_solar_data(api_key, coords, time_start = '2018-01-01', time_end = '2019-01-01')