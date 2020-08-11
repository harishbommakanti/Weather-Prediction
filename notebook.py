#importing modules
#all purpose stuff
import pandas as pd             #for dataframe storage
import numpy as np              #for math
import matplotlib.pyplot as plt #for potential graphing
import json

#ML stuff
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
#--------------------------------------------------------------

X = np.linspace(0,39,num=40).reshape(-1,1) #will always be only 40 measurements

with open('test_dataupload.json') as f:
  data = json.load(f)

y = np.array(data['temps'])

plt.plot(X, y)

#--------------------------------------------------------------
svm_model = svm.SVR()
svm_model.fit(X, y)

rf_model = RandomForestRegressor(random_state=0)
rf_model.fit(X,y)

X_predict = np.linspace(40,80, num=40).reshape(-1,1)

svm_predict = svm_model.predict(X_predict)
rf_predict = rf_model.predict(X_predict)

plt.plot(X_predict, svm_predict)
plt.plot(X_predict, rf_predict)

plt.show()