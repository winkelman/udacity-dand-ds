#!/usr/bin/env python
# -*- coding: utf-8 -*-

### INVESTIGATE THE DIFFERENCES BETWEEN RAINY DAY AND NON-RAINY DAY RIDERSHIP 

import numpy as np
import pandas as pd
import scipy.stats
from ggplot import *
from datetime import datetime


def mann_whitney_plus_means(pandas_df):
    
    df = pandas_df
    
    ### We have reason to believe that the entries
    ### on rainy days vs non-rainy days is significantly different.
    ### The distribution on rainy and non-rainy days does not follow a normal distribution
    ### as we saw in the exploratory plot.
    
    
    ### Because it is log-normal we use a non-parametric test instead of a t-test.
    ### To test this we use a Mann-Whitney U test.
    
    # First we are going to reformat the string dates of the dataframe into date objects for ggplot
    #df.DATEn = df.DATEn.apply(lambda date: datetime.strptime(date, '%Y-%m-%d').date())
    # Reformatting date by day of the week...
    #df.DATEn = df.DATEn.apply(lambda date: date.strftime("%A"))
    # This can all be accomplished in one line...
    #df.DATEn = df.DATEn.apply(lambda date: datetime.strptime(date, '%Y-%m-%d').date().strftime("%A"))
    ## OK, we still need an integer for ggplot, as ggplot cannot sort a string as an ordinal
    df.DATEn = df.DATEn.apply(lambda date: datetime.strptime(date, '%Y-%m-%d').date().weekday())
    
    dfs_groupby_rain_day = df.groupby(['rain', 'DATEn'])
    df_total_entries_by_rain_day = dfs_groupby_rain_day[['ENTRIESn_hourly']].aggregate(np.mean)
    df_total_entries_by_rain_day.reset_index(inplace=True)
    print df_total_entries_by_rain_day
    
    gg = ggplot(df_total_entries_by_rain_day, aes('DATEn', 'ENTRIESn_hourly', color='rain')) + geom_point() + geom_line() + \
    scale_x_discrete(breaks=[0,1,2,3,4,5,6,], labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])  + \
    ggtitle('Average Entries by Day of the Week for Rain and No Rain') + xlab('Day') + ylab('Average Entries')
    print gg
    
    
    ### Mann-Whitney U test ###
    
    entries_with_rain = df.ENTRIESn_hourly[df.rain == 1]
    entries_without_rain = df.ENTRIESn_hourly[df.rain == 0]
    with_rain_mean = np.mean(entries_with_rain)
    without_rain_mean = np.mean(entries_without_rain)
    U, p = scipy.stats.mannwhitneyu(entries_with_rain, entries_without_rain)
    
    return with_rain_mean, without_rain_mean, U, p # leave this line for the grader


if __name__ == "__main__":
    filename = 'turnstile_data_master_with_weather.csv'
    turnstile_weather = pd.read_csv(filename)
    print mann_whitney_plus_means(turnstile_weather)
