#!/usr/bin/env python
# -*- coding: utf-8 -*-

### MORE DATA VISUALIZATIONS

import pandas as pd
import numpy as np
from ggplot import *
import matplotlib.pyplot as plt
from datetime import datetime


def plot_weather_data(pandas_df):
    
    df = pandas_df
    
    # A LOOK AT AVERAGE HOURLY EXITS BY HIGHEST TRAFFIC STATIONS
    '''
    dfs_groupby_station = df.groupby('UNIT') 
    df_ridership_by_station = dfs_groupby_station[['EXITSn_hourly']].aggregate(np.sum)
    df_ridership_by_station.reset_index(inplace = True)
    
    high_value = np.percentile(df_ridership_by_station.EXITSn_hourly, 99)
    series_high_ridership_units = df_ridership_by_station.UNIT[df_ridership_by_station.EXITSn_hourly > high_value]
    df_high_ridership_units = df[df.UNIT.isin(series_high_ridership_units)]
    
    dfs_groupby_high_ridership_unit_hour = df_high_ridership_units.groupby(['UNIT', 'Hour'])
    df_high_ridership_by_unit_hour = dfs_groupby_high_ridership_unit_hour[['EXITSn_hourly']].aggregate(np.average)
    df_high_ridership_by_unit_hour.reset_index(inplace=True)
    print df_high_ridership_by_unit_hour
    
    gg = ggplot(df_high_ridership_by_unit_hour, aes('Hour', 'EXITSn_hourly', color='UNIT')) + \
      geom_line() + geom_point() + \
      ggtitle('Average Exits by Hour for Highest Traffic Stations') + xlab('Hour') + ylab('Average Exits')
    print gg
    '''
    
    
    # A LOOK AT TOTAL DAILY ENTRIES BY HIGHEST TRAFFIC STATIONS
    '''
    # First we are going to reformat the string dates of a dataframe copy into datetime objects for ggplot
    df1 = df.copy(deep=True)
    df1.DATEn = df1.DATEn.apply(lambda date: datetime.strptime(date, '%Y-%m-%d').date())
    # '.date()' ensures that we only get a date object without time!
    
    dfs_groupby_station = df1.groupby('UNIT') 
    df_ridership_by_station = dfs_groupby_station[['ENTRIESn_hourly']].aggregate(np.sum)
    df_ridership_by_station.reset_index(inplace = True)
    
    high_value = np.percentile(df_ridership_by_station.ENTRIESn_hourly, 99)
    series_high_ridership_units = df_ridership_by_station.UNIT[df_ridership_by_station.ENTRIESn_hourly > high_value]
    df_high_ridership_units = df1[df.UNIT.isin(series_high_ridership_units)]
    
    dfs_groupby_high_ridership_unit_day = df_high_ridership_units.groupby(['UNIT', 'DATEn'])
    df_high_ridership_by_unit_day = dfs_groupby_high_ridership_unit_day[['ENTRIESn_hourly']].aggregate(np.sum)
    df_high_ridership_by_unit_day.reset_index(inplace=True)
    print df_high_ridership_by_unit_day
    
    #nparray_unique_date = df1.DATEn.unique()
    #pdseries_unique_date = pandas.Series(nparray_unique_date)
    #xmin = pdseries_unique_date.loc[0]
    #xmax = pdseries_unique_date.loc[len(pdseries_unique_date)-1]
    
    gg = ggplot(df_high_ridership_by_unit_day, aes('DATEn', 'ENTRIESn_hourly', color='UNIT')) + geom_point() + geom_line() + \
    ggtitle('Total Entries by Date for Highest Traffic Stations') + xlab('Date') + ylab('Total Entries')
    print gg
    '''
    
    
    # A LOOK AT AVERAGE TRAFFIC BY HOUR
    df.is_copy = False
    df['net_hourly'] = df.ENTRIESn_hourly - df.EXITSn_hourly
    dfs_groupby_hour = df.groupby('Hour')
    # always aggregate over a list!! otherwise a series will be returned and not a dataframe!!
    df_ridership_by_hour = dfs_groupby_hour[['net_hourly']].aggregate(np.average)
    # always reset the index!! otherwise we will not be able to call the subset!!
    df_ridership_by_hour.reset_index(inplace = True)
    gg = ggplot(df_ridership_by_hour, aes('Hour', 'net_hourly')) + geom_point() + geom_line() + \
      ggtitle('Average Traffic by Hour') + xlab('Hour') + ylab('Average Traffic')
    print gg
    
    
if __name__ == "__main__":
    filename = 'turnstile_data_master_with_weather.csv'
    turnstile_weather = pd.read_csv(filename)
    plot_weather_data(turnstile_weather)
