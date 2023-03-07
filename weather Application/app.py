from flask import Flask, render_template, url_for, request
from bs4 import BeautifulSoup
import requests
import json

app = Flask(__name__)

@app.route("/getLatLong")
def getLatLon():
    url="https://ipinfo.io/json?token=de24e39002ba0c"
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    jsonStr = json.loads(str(data))
    jsonDict = dict(jsonStr)
    return jsonDict["loc"]

@app.route('/')
def weather():
    latLonStr=getLatLon()
    latLon = latLonStr.split(',')

    weather_url= "http://api.openweathermap.org/data/2.5/weather?lat="+latLon[0]+"&lon="+latLon[0]+"&appid=5d8ce9b1708db49fe6790f6aed3c0d74"
    pollution_url="http://api.openweathermap.org/data/2.5/air_pollution?lat="+latLon[0]+"&lon="+latLon[1]+"&appid=5d8ce9b1708db49fe6790f6aed3c0d74"
    
    weather_response = requests.get(weather_url)
    poll_response = requests.get(pollution_url)

    weather_data = BeautifulSoup(weather_response.text, 'html.parser')
    poll_data = BeautifulSoup(poll_response.text, 'html.parser')

    weatherJsonDict = json.loads(str(weather_data))
    pollJsonStr = json.loads(str(poll_data))
    pollJsonDict = dict(pollJsonStr)
    AQI = pollJsonDict["list"][0]["main"]

    if AQI["aqi"] == 1:
        airIndex = "Good"
    elif AQI["aqi"] == 2:
        airIndex = "Fair"
    elif AQI["aqi"] == 3:
        airIndex = "Moderate"
    elif AQI["aqi"] == 4:
        airIndex = "Poor"
    elif AQI["aqi"] == 5:
        airIndex = "Very Poor"
    else:
        airIndex = "Error"
    
    temperature = round(weatherJsonDict["main"]["temp"] - 273.15, 1)
    feels_like = round(weatherJsonDict["main"]["feels_like"] - 273.15, 1)

    return render_template('weather.html',temp = temperature, feels_like = feels_like, tempPresHumi = weatherJsonDict["main"], desc = weatherJsonDict["weather"][0], AQI = airIndex)

if __name__ == "__main__":
    app.run(debug=True)