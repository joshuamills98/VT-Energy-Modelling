import pandas as pd
import numpy as np
import re
import os

def parse_data(file_location):
    """Read in timeseries data and return pandas dataframe"""
    df = pd.read_csv(file_location)
    df.rename(columns ={'Unnamed: 0':'date'}, inplace=True)
    df = df[df['date']<'2019-01-01']
    df['date'] = pd.to_datetime(df['date'])
    df.set_index(keys = ['date'], inplace=True)
    return df


def get_coordinates(directory):
    """ Get all the coordinates of interest from a directory file of solar/wind data"""
    coordinates = []
    p1 = re.compile("_(.*)_")
    p2 = re.compile("_((?:\d|\.)*).csv")
    for i in range(len(os.listdir(directory))):
        coordinates.append([float(p1.findall(os.listdir(directory)[i])[0]),
                            float(p2.findall(os.listdir(directory)[i])[0])])
    return coordinates

def make_datetime(df):
    """ Take on a timeseries dataframe and plot the average daily trend """
    df['dow'] = df.index.dayofweek
    df['doy'] = df.index.dayofyear
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['quarter'] = df.index.quarter
    df['hour'] = df.index.hour
    df['woy'] = df.index.weekofyear
    df['dom'] = df.index.day # Day of Month
    dowdict = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    df['weekday'] = df['dow'].map(dowdict)
    return df 


if __name__ == '__main__':
    parse_data('winddata\winddata_51.103_6.037.csv')