#importing modules
#all purpose stuff
import pandas as pd             #for dataframe storage
import numpy as np              #for math
import matplotlib.pyplot as plt #for potential graphing
import requests                 #for openweather API calls at the least

#ML stuff
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import confusion_matrix
#--------------------------------------------------------------

#here the connection will be established to the DB
connection = None

#--------------------------------------------------------------

#loading data into pandas and data preprocessing
data = pd.read_csv(connection) #or read_sql or whatever

#remove data we don't need, like humidity/wind speed
cols_to_remove = ['pressure','humidity','dew_point','uvi','wind_speed']
data.drop(cols_to_remove, axis=1, inplace=True)

#sort the rows in the df by time, and then set the df index to the time
data = data.sort_values('time')
data = data.groupby('time') #group by the time
['temp'].sum().reset_index()

#data.isnull().sum() #hopefully we shouldn't have to worry about null data

#index with time series data
data = data.set_index('time') #set the new index
print(data.index)

#we don't need to resample as we know the data in the DB will be every 3 hrs
y = data['temp']

#--------------------------------------------------------------