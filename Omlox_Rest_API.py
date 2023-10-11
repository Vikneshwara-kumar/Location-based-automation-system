"""Omlox Nothalt Project Description:

In this project we use omlox localization system to get the indoor
location data. Based on the obtained data we have created zones in the
room. The scope of the project is to check the behaviour of the robotino
in defined zones.

Goal:
To navigate the robotino from one location to another with only omlox
wifi tag.

This script allows the user to connect to omlox server and using the omlox
data navigate the robotino from one location to another.

This script requires that `numpy`, `requests`, `keyboard`, `math`, `threading`,
`signal`, `time`, to be installed within the Python environment you
are running this script in.

"""

import requests
import numpy as np


run = True
zone = 0
colli = False




def omlox(omlox_url):
    '''
    Returns the coordinates data in list.

            Parameters:
                    omlox_url: A string

            Modifies:
                    Nothing

            Returns:
                    data (List): List of X,Y,Z i.e coordinates data
    '''
    r = requests.get(url=omlox_url)
    if r.status_code == requests.codes.ok:
        data = r.json()
        #print(X, Y)
        return data
    else:
        raise RuntimeError("Error: get failed", omlox_url)

def Zone(data):
    '''
        Returns a zone number in the form of int

                Parameters:
                        data: A list containing X ,Y ,Z

                Modifies:
                        X, Y, Z values are retrieved from data(list)
                        Based on X & Y zones are determined

                Returns:
                        zone (int): A number for zone identification
    '''
    global zone
    X = data.get('x')
    Y = data.get('y')
    if X < 0.00 and Y < 0.00:
        print("Location: Out of Lab")
        zone = 0
    elif X <= 1.400:
        print("Location: Festo Area")
        zone = 1
    elif X > 2.410 and X <= 8.100:
        print("Location: Working place in Lab")
        zone = 2
    elif X > 8.200 and X <= 10.000:
        print("Location: Creative Room")
        zone = 3
    return zone

def collision(data1,data2):
    '''
        Returns a list with alarm and distance between two devices.

                Parameters:
                        data1: A list containing X ,Y ,Z of device-1


                        data2: A list containing X ,Y ,Z of device-2

                Modifies:
                        X, Y, Z values are retrieved from data1 & data2
                        Based on X ,Y & Z distance between 2 devices are calculated
                        Alarm is triggered if the distance is less than or equal to the threshold

                Returns:
                        limited_distance (none): A numeric value for distance between 2 devices
                        alarm (Bool): Alarm for collision
    '''
    global alarm
    X1 = data1.get('x')
    Y1 = data1.get('y')
    Z1 = data1.get('z')

    X2 = data2.get('x')
    Y2 = data2.get('y')
    Z2 = data2.get('z')

    distance = np.sqrt(np.square((X1 - X2)) + np.square((Y1 - Y2)) + np.square((Z1 - Z2)))
    limited_distance = "{:.3f}".format(distance)
    #print(distance)
    if distance <= 0.5:
        alarm = True
        print(alarm)
    return limited_distance


