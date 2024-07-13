"""
Omlox Nothalt Project Description:

In this project, we use the omlox localization system to get indoor
location data. Based on the obtained data, we have created zones in the
room. The scope of the project is to check the behavior of the robotino
in defined zones.

Goal:
To navigate the robotino from one location to another using only omlox
WiFi tags.

This script allows the user to connect to the omlox server and, using the omlox
data, navigate the robotino from one location to another.

This script requires that `numpy`, `requests`, `keyboard`, `math`, `threading`,
`signal`, and `time` be installed within the Python environment you
are running this script in.
"""

import requests
import numpy as np

# Global variables
run = True
zone = 0
colli = False

def omlox(omlox_url):
    """
    Fetches the coordinates data from the omlox server.

    Parameters:
        omlox_url (str): The URL to the omlox server.

    Returns:
        list: List containing X, Y, Z coordinates data.

    Raises:
        RuntimeError: If the request to the omlox server fails.
    """
    r = requests.get(url=omlox_url)
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        raise RuntimeError("Error: GET request failed", omlox_url)

def Zone(data):
    """
    Determines the zone based on the X and Y coordinates.

    Parameters:
        data (list): List containing X, Y, Z coordinates data.

    Returns:
        int: Zone identification number.
    """
    global zone
    X = data.get('x')
    Y = data.get('y')

    if X < 0.00 and Y < 0.00:
        print("Location: Out of Lab")
        zone = 0
    elif X <= 1.400:
        print("Location: Festo Area")
        zone = 1
    elif 2.410 < X <= 8.100:
        print("Location: Working place in Lab")
        zone = 2
    elif 8.200 < X <= 10.000:
        print("Location: Creative Room")
        zone = 3
    
    return zone

def collision(data1, data2):
    """
    Calculates the distance between two devices and triggers an alarm if the distance is less than or equal to the threshold.

    Parameters:
        data1 (list): List containing X, Y, Z coordinates of device 1.
        data2 (list): List containing X, Y, Z coordinates of device 2.

    Returns:
        str: Formatted distance between the two devices.
        bool: Alarm status for collision.
    """
    global alarm
    X1 = data1.get('x')
    Y1 = data1.get('y')
    Z1 = data1.get('z')

    X2 = data2.get('x')
    Y2 = data2.get('y')
    Z2 = data2.get('z')

    distance = np.sqrt(np.square(X1 - X2) + np.square(Y1 - Y2) + np.square(Z1 - Z2))
    limited_distance = "{:.3f}".format(distance)

    if distance <= 0.5:
        alarm = True
        print("Collision alarm triggered!")
    
    return limited_distance

# Example usage
if __name__ == "__main__":
    omlox_url1 = "http://example.com/omlox1"
    omlox_url2 = "http://example.com/omlox2"

    data1 = omlox(omlox_url1)
    data2 = omlox(omlox_url2)

    zone1 = Zone(data1)
    zone2 = Zone(data2)

    dist = collision(data1, data2)
    print(f"Distance between devices: {dist} meters")
    print(f"Zone 1: {zone1}, Zone 2: {zone2}")
