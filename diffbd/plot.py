import sklearn
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import mlpy
import numpy as np
import matplotlib.pyplot as plt
import re
import string
import json
import collections
import scipy.stats as stats
import os
from statsmodels.sandbox.regression.predstd import wls_prediction_std

def regression(json_data, bandwidth):
    
    latency = []
    rtt_by_size = []

    ## Create arrays of latency values and rtt * size values
    for i in range(0, len(json_data)):
        latency.append(json_data[i]["latency"])
        rtt_by_size.append(json_data[i]["size"] * json_data[i]["rtt"])

    y = np.array(bandwidth).astype(np.float)
    z = np.array(latency).astype(np.float)
    r = np.array(rtt_by_size).astype(np.float)

    data = np.array([rtt_by_size, y])

    ## Perform a linear regression
    ones = np.ones(len(data[0]))
    X = sm.add_constant(np.column_stack((data[0], ones)))
    for ele in data[1:]:
        X = sm.add_constant(np.column_stack((ele, X)))
    results = sm.OLS(z, X).fit()
    print results.summary() 

    

if __name__ == '__main__':

    ## Read bandwidth, rtt, size, and latency data from all of the files in current directory
    bandwidth = []
    json_data = []
    a = re.compile(".*\.txt$")
    for i in os.listdir(os.getcwd()):
        if a.match(i):  # if it's a text file
            data_file = open(i, 'r+')
            json_data.append(json.load(data_file))
            s = re.findall('[0-9.]*', i)
            bandwidth.append(s[0])

    #print bandwidth
    regression(json_data, bandwidth)
    data_file.close()


