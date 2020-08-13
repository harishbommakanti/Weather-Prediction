#importing modules
#all purpose stuff
import pandas as pd             #for dataframe storage
from pandas import DataFrame
from pandas import read_csv
import numpy as np              #for math
import matplotlib.pyplot as plt #for potential graphing
import json

#stats and ML stuff
from scipy.optimize import curve_fit
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error

from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.ar_model import AutoRegResults
from statsmodels.tsa.ar_model import AutoReg
#--------------------------------------------------------------

#out of sample AutoReg method

#can create a differenced dataset: value(t) = observed(t) - observed(t-1)
def difference(data):
    diff = []
    for i in range(1,len(data)):
        value = data[i] - data[i-1]
        diff.append(value)
    return np.array(diff)

#make a prediction given regression coefficients and lag observed
def predict(coef, history):
    prediction = coef[0]
    for i in range(1, len(coef)):
        prediction += coef[i] * history[-i]
    
    return prediction

def AutoRegTrain(series):
    X = difference(series.values)

    #fit the model
    model = AutoReg(X,lags=24)
    model_fit = model.fit()

    #save model to file
    model_fit.save('models/ar_model.pkl')
    # save the differenced dataset
    np.save('models/ar_data.npy', X)
    # save the last ob
    np.save('models/ar_observation.npy', [series.values[-1]])

def AutoRegPredict():
    #load the saved model
    model = AutoRegResults.load('models/ar_model.pkl')
    data = np.load('models/ar_data.npy')
    last_observation = np.load('models/ar_observation.npy')

    #make the prediction
    predictions = model.predict(start=len(data), end=len(data)) #predict the next step out of the sample

    #transform the prediction
    yhat = predictions[0] + last_observation[0]
    #print(f'Prediction: {yhat}')

    updateDataSet(yhat)

    return yhat

#after a prediction, update the differeced dataset and the last observation
def updateDataSet(recentPrediction):
    observation = recentPrediction

    #load the saved data
    data = np.load('models/ar_data.npy')
    last_observation = np.load('models/ar_observation.npy')

    #update and save the differenced observation
    diffed = observation - last_observation[0]
    data = np.append(data, [diffed], axis=0)
    np.save('models/ar_data.npy', data)

    #update and save the real observation
    last_observation[0] = observation
    np.save('models/ar_observation.npy', last_observation)



def make_predictions(filename):
    """Trains the AutoReg model and returns an array of predictions"""
    
    #load the dataset
    series = read_csv(filename, header=0, index_col=0, squeeze=True)
    X = series.values
    #print(series.shape)

    numTimeSteps = 48
    predictions = []

    for i in range(numTimeSteps):
        AutoRegTrain(series) #train based on past data and differenced data
        newPrediction = AutoRegPredict()
        predictions.append(newPrediction) #add new prediction to predictions array

        #update series by adding the new prediction to it, treating it as ground truth data
        series = series.append(pd.Series([newPrediction], index=[len(X)+i]))

    #plot the data to see how feasible it is, seems very feasible

    print("\nA matplotlib graph should have shown up. For the full experience, view it in full screen.\n\nMake sure to close the matplotlib window for the program to terminate.\n")

    X_history = np.linspace(0,len(X),num=len(X))
    X_predict = np.linspace(len(X), len(X)+numTimeSteps-1, num=numTimeSteps)

    plt.plot(X_history, X, label="Hourly data over the past 5 days", color='blue')
    plt.plot(X_predict, predictions, label = "Hourly forecast over next 2 days", color='red', marker='o')
    plt.title(f"Forecast over the next {numTimeSteps} hours (Farenheit) given the past 5 days of data")

    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    plt.xlabel(f"Time from 5 days ago at {current_time} (Hours)")
    plt.ylabel(f"Temperature (Farenheit)")
    
    x_ticks = np.linspace(0, len(series)-1, num=int(len(series)/5))
    plt.xticks(x_ticks, rotation=45)

    y_ticks = np.linspace(50,110,num=30)
    plt.yticks(y_ticks)

    plt.legend(loc='upper right')

    plt.show()


    return predictions

#make_predictions()












#--------------------------------------------------------------
#other methods that didn't work out as well as I would've thought

def inSampleARIMA():
    df = pd.read_csv('dataupload.csv', header=0, index_col=0, squeeze=True)
    #print(df)
    #df.plot()
    #autocorrelation_plot(df)
    #plt.show()

    X = df.values
    print(X)
    #--------------------------------------------------------------

    #since conventional regression and curve fitting don't match, try to do ARIMA time series stuff

    #fit the model
    model = ARIMA(df, order=(5,1,0))
    model_fit = model.fit(disp=0)
    #print(model_fit.summary())


    #plot residual errors
    residuals = DataFrame(model_fit.resid)
    #residuals.plot() #shows trend info not captured by model
    #plt.show()
    #residuals.plot(kind='kde') #errors are guassian, may not be centered on zero
    #plt.show()
    #print(residuals.describe)
    #--------------------------------------------------------------

    #now, can forecast future timesteps using ARIMA

    #indices of the ARIMAResults object are relative to the start of the training dataset, should be 41 etc

    #size = int(len(X)-1) #make training set only 2/3 of the data
    #train, test = X[0:size], X[size:]
    history = [i for i in X] #[x for x in train]

    num_pred = 48
    X_predict = [len(X)+i for i in range(num_pred)]
    predictions = list()

    for i in range(num_pred):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        history.append(yhat)

    """
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
    """
    #plot

    plt.plot(X)
    plt.plot(X_predict, predictions, color='red')
    plt.show()

    #--------------------------------------------------------------

def scipy_curvefit():
    t = np.linspace(0,39,num=40).reshape(-1,1) #will always be only 40 measurements

    with open('test_dataupload.json') as f:
        jsonfile = json.load(f)

    data = np.array(jsonfile['temps'])
    
    
    guess_freq = 1
    guess_amplitude = 3*np.std(data)/(2**0.5)
    guess_phase = 0
    guess_offset = np.mean(data)

    p0=[guess_freq, guess_amplitude,
        guess_phase, guess_offset]

    # create the function we want to fit
    def my_sin(x, freq, amplitude, phase, offset):
        return np.sin(x * freq + phase) * amplitude + offset

    # now do the fit
    fit = curve_fit(my_sin, t.ravel(), data.ravel(), p0=p0)

    # we'll use this to plot our first estimate. This might already be good enough for you
    data_first_guess = my_sin(t, *p0)

    # recreate the fitted curve using the optimized parameters
    data_fit = my_sin(t, *fit[0])

    plt.plot(data)
    plt.plot(data_fit, label='after fitting')
    plt.plot(data_first_guess, label='first guess')
    plt.legend()
    plt.show()