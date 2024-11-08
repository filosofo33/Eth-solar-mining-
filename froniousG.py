import datetime
import json
import requests
import xml.etree.cElementTree as et
import time
from subprocess import call

def start_mining():
    call(["/opt/ethos/bin/minestart"])

def stop_mining():
    call(["/opt/ethos/bin/minestop"])
    time.sleep(5)
    call(["/opt/ethos/bin/disallow"])
    
def get_solar_data():
    """Get Fronius solar panel data"""
    try:
        response = requests.get("http://192.168.0.200/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
        data = json.loads(response.text)
        return data["Body"]["Data"]["Site"]["P_PV"], data["Body"]["Data"]["Site"]["P_Grid"] + data["Body"]["Data"]["Site"]["P_PV"]
    except:
        return 0, 10

gpus_running = 0
current_day = 0
cloud_update_counter = 0

today = datetime.datetime.now()
print(today.hour)
print(today.day)

# Update weather data daily
if(current_day != today.day or cloud_update_counter == 0):
    cloud_update_counter = 12
    print("Updating weather data")
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=XXXXX&lon=XXXXXXX")
    weather_data = json.loads(response.text)

    sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise'])
    print(sunrise.hour)
    print(sunrise.minute)

    sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset'])
    print(sunset.hour)
    print(sunset.minute)
    print(sunset.month)

    cloud_cover = float(weather_data['clouds']['all'])/100
    current_day = sunset.day
    print(current_day)
    print(cloud_cover)

# Check if it's night time rate period
if((today.hour >= 22) or (today.hour <= 12)):
    print("Starting mining - Night rate period")
    start_mining()
else:
    solar_generation = get_solar_data()
    print(solar_generation[0])
    print(solar_generation[1])
    
    # Check if generating enough solar power
    if(solar_generation[0] > 200):
        print("Starting mining - Sufficient solar generation")
        start_mining()
    else:
        # Check if consuming too much power
        if(solar_generation[1] > 300):
            print("Stopping mining - High power consumption")
            stop_mining()
        else:
            # Check if before sunset
            if(today.hour < sunset.hour or (today.hour == sunset.hour and today.minute < sunset.minute)):
                # Get sun position data from Wolfram Alpha
                wolfram_response = requests.get("http://api.wolframalpha.com/v2/query?appid=XXXXXX&input=sun+azimuth+and+altitude+XXXXXXXXN&format=plaintext")
                wolfram_data = wolfram_response.text.encode("utf8")
                tree = et.fromstring(wolfram_data)

                skip_first = False
                sun_angles = []
                for pod in tree.findall('pod'):
                    print("---")
                    for child in pod.getchildren():
                        for subchild in child.getchildren():
                            if(skip_first):
                                data_lines = subchild.text.splitlines()
                                for line in data_lines:
                                    angle_values = line.split()
                                    sun_angles.append(float(angle_values[2]))
                            else:
                                skip_first = True

                # Calculate adjusted sun angle
                sun_angles[0] = abs(sun_angles[0] - 180)
                sun_angles[1] = abs(sun_angles[1] - 30)  # Less important angle adjustment
                print(sun_angles)
                total_angle = sum(sun_angles)
                total_angle = total_angle + (total_angle * (cloud_cover/2))  # Adjust for cloud cover
                print(total_angle)

                if(total_angle < 85):
                    print("Starting mining - Good sun position")
                    start_mining()
                else:
                    print("Stopping mining - Poor sun position")
                    stop_mining()
            else:
                print("Stopping mining - After sunset")
                stop_mining()
