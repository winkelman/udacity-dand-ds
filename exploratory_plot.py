#!/usr/bin/env python
# -*- coding: utf-8 -*-

### DETERMINE THE NATURE OF THE DISTRIBUTION OF RIDERSHIP

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def entries_histogram(pandas_df):
    
    df = pandas_df
    
    ### Let's plot two histograms on the same axes to show hourly
    ### entries when raining vs. when not raining.
    
    ### no axis transform...
    plt.figure()
    df.ENTRIESn_hourly[df.rain == 1].plot(kind='hist', stacked=True, alpha=0.5, bins=100)
    df.ENTRIESn_hourly[df.rain == 0].plot(kind='hist', stacked=True, alpha=0.5, bins=100)
    plt.xlabel('Entries Hourly')
    plt.ylabel('Frequency')
    plt.xlim([0, 15000])
    plt.ylim([0, 50000])
    plt.show()
    # this command would close the plot
    # plt.clf()
    
    ### with a log scale transform on the x-axis...
    plt.figure()
    df.ENTRIESn_hourly[df.rain == 1].plot(kind='hist', stacked=True, alpha=0.5, bins=np.logspace(0.1, 6, 50)) # your code here to plot a historgram for hourly entries when it is raining
    df.ENTRIESn_hourly[df.rain == 0].plot(kind='hist', stacked=True, alpha=0.5, bins=np.logspace(0.1, 6, 50)) # your code here to plot a historgram for hourly entries when it is not raining
    plt.xlabel('Entries Hourly')
    plt.ylabel('Frequency')
    plt.gca().set_xscale("log")
    plt.show()


if __name__ == "__main__":
    filename = 'turnstile_data_master_with_weather.csv'
    turnstile_weather = pd.read_csv(filename)
    entries_histogram(turnstile_weather)
