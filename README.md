# knitlib-webserver

Knitlib Web server is a Knitlib client that provides REST API endpoints for Knitting Machine software and control.  
Knitlib Webserver is designed to interact with [Knitweb](https://github.com/fashiontec/knitweb)

## Requirements
Knitlib Web requires the Knitlib library to be installed and Flask as main dependencies. Check requirements.txt for more.

## Functionality

Knitlib Web also provides API implementation of Knitlib's async callbacks via Web Sockets in order to handle communication from Knitting Machines to User Facing apps, allowing real time notification of critical errors, warnings, informational messages or blocking operations (e.g. set needle positions, ensure carriage is ready, etc)
