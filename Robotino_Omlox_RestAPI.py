import requests
import sys
import time
import math
import keyboard
from Omlox_Rest_API import omlox, Zone, collision

run = True
zone = True
Collision = False

# Get user inputs for IP addresses and OMLOX Tag IDs
ROBOTINOIP = str(input("Enter the IP address of Robotino: "))
OMLOXIP = str(input("Enter the IP address of OMLOX system: "))
OMLOX_Tag_ID_1 = str(input("Enter the MAC ID number of OMLOX WiFi tag for Robotino: "))
OMLOX_Tag_ID_2 = str(input("Enter the MAC ID number of OMLOX WiFi tag: "))
Zone_ID = str(input("Enter the destination zone ID (zone-1, zone-2, zone-3): "))

# Construct URLs for OMLOX tags
omlox_url1 = f"http://{OMLOXIP}/json/device/{OMLOX_Tag_ID_1}/position"
omlox_url2 = f"http://{OMLOXIP}/json/device/{OMLOX_Tag_ID_2}/position"

def Omlox_system():
    """
    Returns boolean value based on the calculation i.e. When the robotino enters the desired zone it returns true, else false.
    """
    try:
        robotino_data = omlox(omlox_url1)
        omlox_Tag_data = omlox(omlox_url2)
        current_zone_robotino = Zone(robotino_data)
        current_zone_tag = Zone(omlox_Tag_data)
        print(f"The robotino is in zone: {current_zone_robotino}")
        print(f"The omlox tag is in zone: {current_zone_tag}")

        Collision = collision(robotino_data, omlox_Tag_data)
        print(f"Collision: {Collision}")

        if robotino_data == 0:
            print("Location: CPS Machine - 1")
            return True
        elif robotino_data == 1 and Zone_ID == "Zone-1":
            print("Location: Festo mini factory")
            return True
        elif robotino_data == 2 and Zone_ID == "Zone-2":
            print("Location: CPS Machine - 2")
            return True
        elif robotino_data == 3 and Zone_ID == "Zone-3":
            print("Location: CPS Machine - 3")
            return True
        else:
            return False
    except Exception as e:
        print(f"Error in Omlox_system: {e}")
        return False

def set_vel(vel):
    """
    Sets the velocity of the Robotino.

    Parameters:
        vel (list): A list containing velocity values.
    """
    OMNIDRIVE_URL = f"http://{ROBOTINOIP}/data/omnidrive"
    try:
        r = requests.post(url=OMNIDRIVE_URL, json=vel)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error in set_vel: {e}")
        raise RuntimeError(f"Error: post to {OMNIDRIVE_URL} with params {vel} failed")

def bumper():
    """
    Returns the bumper sensor value from the Robotino.

    Returns:
        float: Bumper sensor value.
    """
    BUMPER_URL = f"http://{ROBOTINOIP}/data/bumper"
    try:
        r = requests.get(url=BUMPER_URL)
        r.raise_for_status()
        data = r.json()
        return data["value"]
    except requests.exceptions.RequestException as e:
        print(f"Error in bumper: {e}")
        raise RuntimeError(f"Error: get from {BUMPER_URL} failed")

def distances():
    """
    Returns an array of distance sensor outputs from the Robotino.

    Returns:
        dict: Distance sensor outputs.
    """
    DISTANCES_URL = f"http://{ROBOTINOIP}/data/distancesensorarray"
    try:
        r = requests.get(url=DISTANCES_URL)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in distances: {e}")
        raise RuntimeError(f"Error: get from {DISTANCES_URL} failed")

def motion(vec, deg):
    """
    Rotates vector vec by deg degrees and returns the rotated vector as a list.

    Parameters:
        vec (list): A list containing vector values.
        deg (float): Rotation angle in degrees.

    Returns:
        list: Rotated vector.
    """
    rad = 2 * math.pi / 360 * deg  # Corrected to 360 degrees for full circle

    out = [0, 0]
    out[0] = math.cos(rad) * vec[0] - math.sin(rad) * vec[1]
    out[1] = math.sin(rad) * vec[0] + math.cos(rad) * vec[1]

    return out

def main():
    try:
        startVector = [0.2, 0.0]
        a = 0
        msecsElapsed = 0
        vec = [0, 0, 0]

        while not bumper() and run and not Omlox_system() and not Collision:
            dir = motion(startVector, a)
            vec[0] = dir[0]
            vec[1] = dir[1]
            set_vel(vec)
            time.sleep(0.05)
            msecsElapsed += 50

        set_vel([0, 0, 0])
    except Exception as e:
        print(f"Error in main: {e}")
        if keyboard.is_pressed("q"):
            sys.exit()
        return 1
    return 0

if __name__ == '__main__':
    main()
    sys.exit(0)
