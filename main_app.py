from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

import time
import requests
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def main():
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    return render_template("homepage.html")

def loadPastData():
    pastTimes = getPastTimes() #past 5 days in UNIX time

    zipcode = "78613" #change to get form input later
    lat, lon = getLatLong(zipcode)
    
    weatherApiKey = 'ef49a66f02393c65eb96e511aa8a7898'; #harish's api key

    all_data = []
    for i in range(len(pastTimes)):
        time = pastTimes[i]
        url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={weatherApiKey}'

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
        faren = (9/5) * kelvin - 459.67

        temperatures.append(faren)
    
    return temperatures

if __name__ == "__main__":
    app.run()
    #pastData = loadPastData()
    #print(pastData)