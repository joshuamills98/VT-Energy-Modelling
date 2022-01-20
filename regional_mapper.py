import pandas as pd
from helper_functions import *
from shapely.geometry import shape, Point
from IPython.display import display
import numpy as np
import folium
import json

def get_averages(directory):
    """ Return a df of the average capacity factor at the given location"""
    output_list = []
    coordinates = get_coordinates(directory)
    for i,file in enumerate(os.listdir(directory)):
        df = parse_data(os.path.join(directory,file))
        mean = df['electricity'].mean()
        point = Point(coordinates[i][1], coordinates[i][0])
        output_list.append([find_region_of_NL(point), 
                            coordinates[i][0], coordinates[i][1], 
                            mean]) # append respecive region, lat, long and mean CF
    df = pd.DataFrame(data = output_list, columns = ['Region', 'latitude', 'longitude', 'mean_CF'])
    return df


def find_region_of_NL(point):
    province_path = os.path.join('NL_provinces','provinces.geojson')
    with open(province_path) as f:
        js = json.load(f)

    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature["properties"]["name"]

def map_regional_data(geojson_data_path,
                      data,
                      save_name):
    communities_map = folium.Map(location=[52.5280, 5.5954],
                                 tiles='stamenterrain',
                                 zoom_start=7.2)
    chloro = folium.Choropleth(
        geo_data=geojson_data_path,
        name='choropleth',
        data=data,
        fill_color='{}'.format('BuPu'),
        fill_opacity=0.7,
        columns=['Region','mean_CF'],
        key_on='feature.properties.name',
        highlight=True,
        legend_name='Mean Capacity Factor',
        bins = list(np.linspace(0.0,0.6,10))).add_to(communities_map)
    style_function = "font-size: 15px; font-weight: bold"
    folium.features.GeoJsonTooltip(
            ['name'],
            style=style_function,
            labels=False).add_to(chloro.geojson)
    folium.LayerControl().add_to(communities_map)
    display(communities_map)
    # communities_map.save(outfile= os.path.join('Plots', save_name))

if __name__ == '__main__':
    province_path = os.path.join('NL_provinces','provinces.geojson')
    map_regional_data(province_path,
                      get_averages('./winddata/'),
                      'WindCapacityPlot.html')