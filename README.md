# Location based automation system 

### Project Description:
In this project, I've implemented a location-based automation system, harnessing the capabilities of 5G technology. In detail, I've utilized indoor localization for precise navigation and have applied the geofencing technique to control the operation of the automation system within a shop floor. An Automated Guided Vehicle (AGV) is driven based on the indoor localization system, specifically Omlox, and a conveyor system has been integrated with an Omlox Wi-Fi tag to establish the static location of assets.

This module provides functions to establish a connection with an Omlox server and navigate within the area using data from the localization system. The project involves the creation of distinct zones within the designated area and enables the robot to autonomously approach the conveyor system, retrieve products, and transport them to other locations.

## Dependencies:
This module requires the following packages to be installed in the Python environment: numpy, requests, keyboard, math, threading, signal, and time.

## Functions:

### omlox(omlox_url): 
Sends a GET request to the Omlox server specified by the omlox_url parameter and returns a list of the X, Y, and Z coordinates data.

### Zone(data): 
Takes in a list containing the X, Y, and Z values and determines the zone of the location. Returns an integer representing the zone.

### collision(data1, data2): 
Takes two lists containing coordinates data of two devices and calculates the distance between them. If the distance is less than or equal to a threshold value of 0.5, an alarm is triggered and the function returns the distance value.

### bumper()
This function gets the current state of the Robotino's bumper. It returns True if the bumper is pressed, otherwise it returns False.


## Global Variables:

1. zone: An integer representing the current zone.
2. colli: A boolean variable indicating if a collision has occurred.
3. alarm: A boolean variable indicating if an alarm should be triggered.

### Note:
This module does not provide a full implementation of the Omlox Nothalt Project. It only provides the core functionalities for connecting to the Omlox server and navigating the AGV or any other stuff based on the obtained data.


## How to use the Omlox Module.
1. Setup the python environvnment with all the dependencies.
2. Python script Omlox_Rest_API is collection of funtions of the omlox system. Using REST API it access the Omlox hub using the provided URL (http:\\xxx.xx.x.xxx),extracts the Location data of specific Tag.
3. Accuracy_test script is used for collecting the location data, visualize the data and calculate its accuracy  
4. DataProcessing is a script used to process the stored JSON data this is a dependency for ACCURACY_test scrip
