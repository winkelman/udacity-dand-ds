#!/usr/bin/env python
# -*- coding: utf-8 -*-

### INSPECT THE MODEL RESIDUALS

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
from model_fit import predictions


def plot_residuals(pandas_df, predictions):
	
    df = pandas_df
    
    # This would give us an overlay of predictions and the hourly entries as a histogram....
    plt.figure()
    predictions = pd.Series(predictions)
    predictions.plot(kind='hist', stacked=True, alpha=0.5, bins=100)
    df.ENTRIESn_hourly.plot(kind='hist', stacked=True, alpha=0.5, bins=100)
    #plt.xlim([-15000, 15000])
    #plt.ylim([0, 2500])
    # We can see that our model predicts some negative values for hourly entries
    
    
    # We can see that frequency of residuals is zero mean and APPEARS gaussian
    #make sure both types are pandas series
    #print type(predictions), type(df.ENTRIESn_hourly)
    error = df.ENTRIESn_hourly - predictions
    plt.figure()
    error.hist(bins=100)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    
    plt.figure()
    error.plot()
    plt.xlabel('Data')
    plt.ylabel('Residuals')
    plt.show()   
    
    
# A probability plot (somewhat similar to a Q-Q plot) to compare our residuals to a gaussian distribution (gaussian by default if not specified)
def prob_plot_residuals(pandas_df, predictions):
    
    df = pandas_df
    plt.figure()
    scipy.stats.probplot(df['ENTRIESn_hourly'] - predictions, plot=plt)
    plt.show()

    
if __name__ == "__main__":
    filename = 'turnstile_data_master_with_weather_short.csv'
    turnstile_weather = pd.read_csv(filename)
    predictions = predictions(turnstile_weather)
    plot_residuals(turnstile_weather, predictions)
    prob_plot_residuals(turnstile_weather, predictions)
    