import time
import requests
import pandas as pd
import re

#for openweathermap
weather_api_key = 'ef49a66f02393c65eb96e511aa8a7898' #harish's api key

def loadPastData(lat, lon):
    pastTimes = getPastTimes() #past 5 days in UNIX time

    all_data = []
    for i in range(len(pastTimes)):
        time = pastTimes[i]
        url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={weather_api_key}'

        daily_temps = performOpenWeatherAPICall(url)
        all_data.extend(daily_temps)
    
    return all_data





def getPastTimes():
    currTime = time.time()
    dayInSeconds = 24*60*60
    pastTimes = []

    for i in range(5):
        pastTimes.append(int(currTime - dayInSeconds*i)) #get rid of decimal for seconds
    
    return pastTimes

def getLatLong(zip):
    applicationApiKey = 'hKzocZfFBzwpJU0NImyynukV7g7RnN3aH8tX2WWc6woz2VJy8ecyYJCr1aQtb0FJ'

    url = f"https://www.zipcodeapi.com/rest/{applicationApiKey}/info.json/{zip}/degrees"

    response = requests.get(url).json()

    return [response['lat'], response['lng']]

def performOpenWeatherAPICall(url):
    response = requests.get(url).json()
    
    hourly_data_arr = response['hourly']

    temperatures = []

    for i in range(len(hourly_data_arr)):
        kelvin = hourly_data_arr[i]['temp']
        temperatures.append(to_faren(kelvin))
    
    return temperatures

def to_faren(kelvin):
    """Converts from kelvin to farenheit"""
    return int((9/5) * kelvin - 459.67)

def get_future_forecast(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={weather_api_key}'

    response = requests.get(url).json()

    hourly_data = response['hourly']

    correct_forecast = []

    for i in range(len(hourly_data)):
        kelvin = hourly_data[i]['temp']
        correct_forecast.append(to_faren(kelvin))
    
    return correct_forecast


if __name__ == "__main__":
    zipcode = str(input("Welcome to Weather Prediction. Enter a US zip code (5 digits) and a graphic will be generated of the program generated temperature forecast as well as the forecast done by OpenWeather's API for the next 48 hours.\n"))
    
    #make sure that zipcode is valid
    test_coords = 30.5052, -97.82
    lat, lon = test_coords
    
    flag = True
    while flag:
        try:
            lat, lon = getLatLong(zipcode)
            flag = False
        except:
            zipcode = str(input("Please make sure you enter a valid US zip code. Keep in mind that some zip codes like 41376 are not available for the forecast due to the APIs.\n"))
    
    #load the past data
    pastData = loadPastData(lat, lon)

    #generate a local csv for the notebook to operate on
    with open('dataupload.csv', 'w') as f:
        f.write('dt,temp\n')

        for i in range(len(pastData)):
            f.write(f"{i},{pastData[i]}\n")
    
    #record openweather predictions
    openweather_preds = get_future_forecast(lat, lon)

    #import notebook.py and do that, generating matplotlib graphics
    from notebook import make_plot_predictions
    make_plot_predictions("dataupload.csv", openweather_preds)