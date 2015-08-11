#!/bin/bash
gunicorn -k flask_sockets.worker knitlib_webserver:app
