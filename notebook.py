#importing modules
#all purpose stuff
import pandas as pd             #for dataframe storage
from pandas import DataFrame
import numpy as np              #for math
import matplotlib.pyplot as plt #for potential graphing
import json
from scipy.optimize import curve_fit
from pandas.plotting import autocorrelation_plot
from sklearn.metrics import mean_squared_error

#ML stuff
from statsmodels.tsa.arima_model import ARIMA
#--------------------------------------------------------------

def inSampleARIMA():
    df = pd.read_csv('test_dataupload.csv', header=0, index_col=0, squeeze=True)
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
    plt.show()
    #residuals.plot(kind='kde') #errors are guassian, may not be centered on zero
    plt.show()
    #print(residuals.describe)
    #--------------------------------------------------------------

    #now, can forecast future timesteps using ARIMA

    #indices of the ARIMAResults object are relative to the start of the training dataset, should be 41 etc

    #size = int(len(X)-1) #make training set only 2/3 of the data
    #train, test = X[0:size], X[size:]
    history = [i for i in X] #[x for x in train]

    num_pred = 20
    X_predict = [40+i for i in range(num_pred)]
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