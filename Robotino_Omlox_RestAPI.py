import requests
import sys
import time
import math
import keyboard
from Omlox_Rest_API import omlox
from Omlox_Rest_API import Zone
from Omlox_Rest_API import collision



run = True
zone = True
Collison = False

# Python program showing
ROBOTINOIP = str(input("Enter the IP address of Robotino: "))
print(ROBOTINOIP)

OMLOXIP = str(input("Enter the IP address of OMLOX system: "))
print(OMLOXIP)

OMLOX_Tag_ID_1 = str(input("Enter the mac id number of omlox wifi tag for Robotino: "))
print("OMLOX_Tag_ID_1:",OMLOX_Tag_ID_1)

OMLOX_Tag_ID_2 = str(input("Enter the mac id number of omlox wifi tag: "))
print("OMLOX_Tag_ID_2:",OMLOX_Tag_ID_2)

Zone_ID = str(input("Enter the destination zone id (zone-1, zone-2, zone-3)\n"))
print(Zone_ID)

omlox_url1 = "http://" + OMLOXIP + "/json/device/" + OMLOX_Tag_ID_1 + "/position"   ##URL for robotino OMLOX TAG
omlox_url2 = "http://" + OMLOXIP + "/json/device/" + OMLOX_Tag_ID_2 + "/position"   ##URL for 2nd OMLOX TAG

def Omlox_system():
    '''
        Returns boolean value based on the calculation i.e When the robotino enters the desired zone it returns a true else the return value will be false.

            Returns:
                    Zone (Bool): True or false based on the calculation.
    '''

    robotino_data = omlox(omlox_url1)
    omlox_Tag_data = omlox(omlox_url2)
    current_zone_robotino = Zone(robotino_data)
    current_zone_tag = Zone(omlox_Tag_data)
    print("The robotino is in zone:",current_zone_robotino)
    print("The omlox tag is in zone:", current_zone_tag)

    Collison = collision(robotino_data,omlox_Tag_data)
    print(Collison)
    if robotino_data==0:
        print("Location: CPS Machine - 1")
        zone = True
    elif robotino_data== 1 and Zone_ID == "Zone-1":
        print("Location: Festo mini factory ")
        zone = True
    elif robotino_data== 2 and Zone_ID == "Zone-2":
        print("Location: CPS Machine - 2")
        zone = True
    elif robotino_data== 3 and Zone_ID == "Zone-3":
        print("Location: CPS Machine - 3")
        zone = True
    else:
        zone = False

    return zone

def set_vel(vel):
    '''
            Parameters:
                    vel (int): A decimal integer

    '''
    OMNIDRIVE_URL = "http://" + ROBOTINOIP + "/data/omnidrive"
    r = requests.post(url=OMNIDRIVE_URL, json=vel)
    if r.status_code != requests.codes.ok:
        # print("Error: post to %s with params %s failed", OMNIDRIVE_URL, PARAMS)
        raise RuntimeError("Error: post to %s with params %s failed", OMNIDRIVE_URL)


def bumper():
    '''
    Returns float value from the bumper sensors output from the robotino

            Returns:
                    data (float): variable sensor values
    '''
    BUMPER_URL = "http://" + ROBOTINOIP + "/data/bumper"
    r = requests.get(url=BUMPER_URL)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data["value"]
    else:
        raise RuntimeError("Error: get from %s with params %s failed", BUMPER_URL)


def distances():
    '''
    Returns a array of distance sensor output from robotino.

            Returns:
                    data (array): Array of distance sensor output.
    '''
    DISTANCES_URL = "http://" + ROBOTINOIP + "/data/distancesensorarray"
    r = requests.get(url=DISTANCES_URL)
    if r.status_code == requests.codes.ok:
        data = r.json()
        return data
    else:
        raise RuntimeError("Error: get from %s with params %s failed", DISTANCES_URL)


# rotate tuple vec by deg degrees and return the rotated vector as a list
def motion(vec, deg):
    '''
    Returns the calculated output of vec and deg.

            Parameters:
                    vec (int): A decimal integer
                    deg (int): Another decimal integer

            Returns:
                    out (int): calculated output of vec and deg
    '''
    rad = 2 * math.pi / 380 * deg

    out = [0, 0]

    out[0] = (math.cos(rad) * vec[0] - math.sin(rad) * vec[1])
    out[1] = (math.sin(rad) * vec[0] + math.cos(rad) * vec[1])

    return out


def main():
    try:
        startVector = (0.2, 0.0);
        a = 0;
        msecsElapsed = 0;
        vec = [0, 0, 0];

        while False == bumper() and True == run and False == Omlox_system() and False == Collison :
            dir = motion(startVector, a);

            vec[0] = dir[0];
            vec[1] = dir[1];

            set_vel(vec);

            time.sleep(0.05)
            msecsElapsed += 50;

        set_vel([0, 0, 0])

    except Exception as e:
        print(e)
        if keyboard.is_pressed("q"):
            print(keyboard.is_pressed("q"))
            sys.exit()
        return 1

    return 0


if __name__ == '__main__':
    main()
    sys.exit(0)