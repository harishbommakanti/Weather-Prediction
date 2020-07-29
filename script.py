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
h1 = requests.get("https://samples.openweathermap.org/data/2.5/history/city?lat=41.85&lon=-87.65&appid=b1b15e88fa797225412429c1c50c122a1") #example API call for openweather