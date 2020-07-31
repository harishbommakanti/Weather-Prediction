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

data = pd.read_csv(connection) #mb change it to read_sql or whatever
all_Y = data["temp"]
all_X = data.drop("temp")

#split the data using sklearn train_test split
X_train, X_test, Y_train, Y_test = train_test_split(all_X,all_Y,random_state=42)

#use sklearn feature importance to determine most important features
#train forest classifier on training data
importance_regressor = RandomForestRegressor()
importance_regressor.fit(X_train,Y_train) #fit the data on the training data
importance_regressor.score(X_test,Y_test) #score the data based on testing data

#add the feature importance in
feature_importances = pd.DataFrame(importance_regressor.feature_importances_,
                                   index = X_train.columns, columns=['importance']).sort_values('importance',ascending=False)

#the features with the highest scores will have the most impact on predicting the data
print(feature_importances)

features = [] #TODO populate this with most important features
X = all_X[features]

#update the training/testing sets off of revised dataset
X_train, X_test, Y_train, Y_test = train_test_split(X,all_Y,test_size=0.2)

#--------------------------------------------------------------

#calls for the regression models
#calls for the regression models

#svm
svm_model = svm.SVR(C=1.0,epsilon=0.2)
svm_model.fit(X_train,Y_train)
svm_predictions = svm_model.predict(X_test)

#random forest
rf_model = RandomForestRegressor(max_depth = 5, random_state=0)
rf_model.fit(X_train,Y_train)
rf_predictions = rf_model.predict(X_test)

#linear regressor
lin_model = LinearRegression()
lin_model.fit(X_train,Y_train)
lin_predictions = lin_model.predict(X_test)

#ridge regression
ridge_model = linear_model.Ridge(alpha=0.5)
ridge_model.fit(X_train,Y_train)
ridge_predictions = ridge_model.predict(X_test)

#bayesian regression
bay_model = linear_model.BayesianRidge()
bay_model.fit(X_train,Y_train)
bay_predictions = bay_model.predict(X_test)

#--------------------------------------------------------------

#assess the accuracy
#R squared values
print("svm r squared: ",r2_score(Y_test,svm_predictions))
print("random forest r squared: ",r2_score(Y_test,rf_predictions))
print("linear regression r squared: ",r2_score(Y_test,lin_predictions))
print("ridge r squared: ",r2_score(Y_test,ridge_predictions))
print("bayes r squared: ",r2_score(Y_test,bay_predictions),"\n")

#make sure no overfit is happening by using cross validation
svm_cvmodel = svm.SVR(C=1.0,epsilon=0.2)
rf_cvmodel = RandomForestRegressor(max_depth = 5, random_state=0)
lin_cvmodel = LinearRegression() #bayes and ridge regression are basically this anyways, will just use this to check CV

print("cross validations: \n")
scores = cross_val_score(svm_cvmodel,X,all_Y,cv=10,scoring="r2") #gives 10 different scores
print("svm: ",np.mean(scores))
scores = cross_val_score(rf_cvmodel,X,all_Y,cv=10,scoring="r2") #gives 10 different scores
print("random forest: ",np.mean(scores))
scores = cross_val_score(lin_cvmodel,X,all_Y,cv=10,scoring="r2") #gives 10 different scores
print("lin regression: ",np.mean(scores))