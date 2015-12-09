#!/usr/bin/env python
# -*- coding: utf-8 -*-

### PERFORM LINEAR REGRESSION AND APPROXIMATE RIDERSHIP USING FEATURES OF INTEREST

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def ols_estimation(features, values):
    
    ### Perform Ordinary Least Squares Estimation of Linear Coeffcicients
    
    # Allows us to see the dimensions of the matrix Xt*X before we attempt to invert
    #Xt_X = np.dot(numpy.transpose(features_array), features_array)
    #print Xt_X.shape
    
    # Gives the determinant 
    #print np.linalg.det(Xt_X)
    
    # Taking the pseudo-inverse as the matrix is sometimes singular (zero determinant)
    inverse_term = np.linalg.pinv( np.dot(np.transpose(features), features) )
    final_term = np.dot(inverse_term, np.transpose(features))
    beta = np.dot(final_term, values)
    
    return beta


def normalize_features(df):
   
    mu = df.mean()
    sigma = df.std()
    
    if (sigma == 0).any():
        raise Exception("One or more features had the same value for all samples, and thus could " + \
                         "not be normalized. Please do not include features with only a single value " + \
                         "in your model.")
    df_normalized = (df - df.mean()) / df.std()

    return df_normalized, mu, sigma


def compute_r_squared(values, predictions):

    mean_of_values_array = values.mean() * np.ones(len(values))
    ss_res = np.square(values - predictions).sum()
    ss_tot = np.square(values - mean_of_values_array).sum()
    r_squared = 1 - (ss_res/ss_tot)
    
    return r_squared


def predictions(dataframe):
    
    # Select Features (try different features!)
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]
    
    # Add UNIT to features using dummy variables... UNIT is the turnstile location.
    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    #features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
    
    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values)

    # perform OLS estimation, get beta
    beta = ols_estimation(features_array, values_array)
    
    # calculate predicted values based on beta
    predictions = np.dot(features_array, beta)
    
    
    # How many unique stations?
    #nparray_unique_station = dataframe.UNIT.unique()
    #print len(nparray_unique_station)
    # Above is same as length of beta minus our 5 (4 + y-int) hand-picked features
    # Below we can see which beta values correspond to what features...
    #print features.head()
    #print beta
    # Beta and singular numpy arrays are like vectors (top to bottom, not left to right)
    
    
    print "The r-squared value is: ", compute_r_squared(values_array, predictions)
    return predictions


if __name__ == "__main__":
    filename = 'turnstile_data_master_with_weather_short.csv'
    turnstile_weather = pd.read_csv(filename)
    predictions = predictions(turnstile_weather)