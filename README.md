# knitserver

## 1. What is Knit Server
Knitserver is a Knitlib client that provides REST API endpoints for Knitting Machine software and control. Knitserver is designed to interact with [Knitweb](https://github.com/fashiontec/knitweb)

## 2. How to install Knit-Server
### 2.1 Requirements
Knitlib Web requires the Knitlib library to be installed and Flask as main dependencies. Check requirements.txt for more.
### 2.2 Step by Step Installation

Currently there is not a packaged version of Knitserver, however it is quite easy to get up and running.

1. Download the Source Code (either git clone this repository or download a zip or tar).
2. Browse the repo (and optional, setup a virtual enviroment: virtualenv venv )
3. Install the dependencies from requirements.txt ( pip install -r requirements.txt )/if you are using any proxy run: sudo pip install --proxy="http://Your proxy:port" -r requirements.txt

4. Run the server: python knitlib_webserver.py or run.sh

## 3. Knit Server API
Knitlib Web also provides API implementation of Knitlib's async callbacks via Web Sockets in order to handle communication from Knitting Machines to User Facing apps, allowing real time notification of critical errors, warnings, informational messages or blocking operations (e.g. set needle positions, ensure carriage is ready, etc)
* Sample Api Calls and Messages

## 4. Using Knit Server with a Web Interface
Please refer to https://github.com/fashiontec/knitweb
