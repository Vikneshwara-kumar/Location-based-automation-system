# **Location Based Automation System**

## Project Overview
This project implements a location-based automation system leveraging the capabilities of 5G technology and indoor localization. The system uses the Omlox indoor localization system for precise navigation and geofencing to control automation operations within a shop floor. An Automated Guided Vehicle (AGV) navigates based on data from Omlox, and a conveyor system integrated with an Omlox Wi-Fi tag establishes the static location of assets.

## Scope

The scope of the project includes establishing connections with the Omlox server, creating distinct zones within the designated area, and enabling the robot to autonomously approach the conveyor system, retrieve products, and transport them to other locations.

## Key Objectives

*   Utilize indoor localization for precise navigation.
*   Apply geofencing to control operations within defined zones.
*   Enable autonomous navigation of AGV using Omlox Wi-Fi tags.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#Features)
4. [Testing](#Testing)
5. [Contributing](#contributing)
6. [License](#license)
7. [Acknowledgements](#acknowledgements)

## Installation
### Prerequisites
*   Raspberry Pi devices
*   Omlox localiation system
*   Festo AGV
*   5G Modem

### setup  
To set up the environment and install dependencies, use the provided setup_environment.sh script:
chmod +x setup_environment.sh
Clone the repository: 
```
git clone https://github.com/Vikneshwara-kumar/Location Based Automation System.git
```
Navigate to the project directory: 
```
cd Location Based Automation System
```
```
./setup_environment.sh
```

## Usage
1.  Initialize IP Addresses and Tags: Input the IP addresses for Robotino and the Omlox system, as well as the MAC IDs for the Omlox Wi-Fi tags.
2.  Run the Main Script: Execute the main script to start navigating the Robotino using the Omlox localization data.
```
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
```

## Features
*   Omlox Integration: Connects to Omlox server to fetch location data.
*   Zone Identification: Determines and identifies zones based on coordinates.
*   Collision Detection: Calculates distance between devices and triggers an alarm if necessary.
*   Bumper and Distance Sensors: Reads and processes data from Robotino's bumper and distance sensors.
*   Motion Control: Controls Robotino's motion based on calculated vectors.

## Testing
To test the individual components:

1.  Unit Tests: Write unit tests for each function to ensure they work correctly.
2.  Integration Tests: Test the integration of the Omlox system with the Robotino.

##  Contributing
Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create your feature branch (git checkout -b feature/YourFeature).
3.  Commit your changes (git commit -m 'Add some feature').
4.  Push to the branch (git push origin feature/YourFeature).
5.  Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Thanks to the Omlox team for providing the indoor localization system.
Special thanks to the contributors who helped in developing and testing this project.