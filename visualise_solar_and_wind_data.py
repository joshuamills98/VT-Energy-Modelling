import pandas as pd
import numpy as np
import re
import os

def parse_data(file_location):
    df = pd.read_csv(file_location)
    df.rename(columns ={'Unnamed: 0':'date'}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(keys = ['date'], inplace=True)
    return df


""" Helper functions """

def get_coordinates(directory):
    """ Get all the coordinates of interest from a directory file of solar/wind data"""
    coordinates = []
    p1 = re.compile("_(.*)_")
    p2 = re.compile("_((?:\d|\.)*).csv")
    for i in range(len(os.listdir(directory))):

        coordinates.append([float(p1.findall(os.listdir(directory)[i])[0]),
                            float(p2.findall(os.listdir(directory)[i])[0])])
    return coordinates

# def plot_basic(wind_data, solar_data):


if __name__ == '__main__':
    parse_data('winddata\winddata_51.103_6.037.csv')