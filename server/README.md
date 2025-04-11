# IoT Remote Lab for Automation and Control Students
## Overview
This thesis is aimed at providing a simple and web-based platform for interacting with automation and control ...
Divided into 3 main blocks, a web page for user interaction, a webserver for ... and the on-site instalatiing of integraded boards.

## Features
- *Real-time data visualization*
- *Remote control testing and simulation*
- *Experimental data storage*

## Hardware requirements
- Raspberry Pi (or similar small computer)
- Arduino Uno with Arduino MKR Wifi1010/Arduino with wifi capabilities
- 10kΩ resistors

## Installation
### WebServer
This is the installation for the webserver. It's light and can run on a small board computer like a Raspberry Pi or similar.
#### Install Python 
Download and install Python (version 3.x recommended) from [Python's official website](https://www.python.org/downloads/).

Make sure `python` and `pip` are accessible:
```bash
python --version
pip --version
```
####  Install Required Packages
To install the required packages just run this command:
```bash
pip install flask flask_mqtt flask-socketio
```
#### MQTT Broker


### On-site
This is the software and hardware installation connected to the process or processes in the classroom or lab. It's comprized of an *Arduino Uno* and an *Arduino MKR 1010 Wifi* as well as some eletronic logic needed for the communication between the two.
