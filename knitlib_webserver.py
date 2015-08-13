# -*- coding: utf-8 -*-
# This file is part of Knitlib.
#
#    Knitlib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Knitlib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Knitlib.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2015 Sebastian Oliva <http://github.com/fashiontec/knitlib>
__author__ = "tian"

import time
import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from flask_sockets import Sockets, Worker
from flask_cors import cross_origin
from gevent import spawn, sleep
from threading import Thread

import knitlib
from knitlib.knitting_job import KnittingJob

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret'
UPLOAD_FOLDER = '/tmp/knitlib_web_uploads/'
app.config.from_object('config_module.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


sockets = Sockets(app)
# A reference for creating new RESTful endpoints:
# http://blog.luisrei.com/articles/flaskrest.html


job_dict = {}
msg_queue = []
progress = None
thread = None


# if not app.debug:
import logging
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('tmp/knitlib-webserver.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('knitlib-webserver')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/test_operation")
def socket_test_page():
    #TODO: simple page to test REST and Sockets operation.
    return \
'''
<html>

    <head>
        <title>Test</title>

        <script type="text/javascript">
            var ws = new WebSocket("ws://" + location.host + "/echo");
            ws.onmessage = function(evt){
                    var received_msg = evt.data;
                    console.log(received_msg);
            };

            ws.onopen = function(){
                ws.send("hello");
            };

            var create_knitjob = function () {
              knitjob_id = ""
              $.ajax({
                type: "POST",
                dataType: "json",
                url: "//"+location.host + "/v1/create_job/",
                data: {
                  "plugin_id": "dummy",
                  "port": "/dev/null"
                },
                success: function(data){
                  console.log("Created knitting job:")
                  console.log(data);
                  knitjob_id = data["job_id"];
                }
              });
              return knitjob_id;
            };

            var init_knitjob = function (job_id) {
              $.ajax({
                type: "POST",
                dataType: "json",
                url: "//"+location.host + "/v1/init_job/" + job_id,
                data: {
                  /* No data should be needed for job init. */
                },
                success: function(data){
                  console.log("Inited knitting job:")
                  console.log(data);
                }
              });
            };

            var config_knitjob = function (job_id) {
              /**
              var fd = new FormData();
              fd.append("knitpat_dict", {"colors": 2, "file_url":"embedded" });
              */
              $.ajax({
                type: "POST",
                dataType: "json",
                // contentType: false,
                contentType: "multipart/form-data",
                url: "//"+location.host + "/v1/configure_job/" + job_id,
                data: {
                  "knitpat_dict": {"colors": 2, "file_url":"embedded" }
                  // TODO: add image data
                  // "file": new Blob()
                },
                success: function(data){
                  console.log("Configured knitting job:")
                  console.log(data);
                }
              });
            };

            var knit_knitjob = function (job_id) {
              $.ajax({
                type: "POST",
                dataType: "json",
                url: "//"+location.host + "/v1/knit_job/" + job_id,
                data: {
                  /* No data should be needed */
                },
                success: function(data){
                  console.log("Knitting knitting job:")
                  console.log(data);
                }
              });
            };
        </script>

    </head>

    <body>
        <p>Check out the console to test operation.</p>

        <script src="//code.jquery.com/jquery-1.11.3.js"></script>
    </body>

</html>
'''


@app.route('/v1/get_machine_plugins')
@cross_origin()
def get_machine_plugins():
    return jsonify({"active_plugins": knitlib.machine_handler.get_active_machine_plugins_names()})


@app.route('/v1/get_ports')
@cross_origin()
def get_ports():
    port_dict = dict([(p[0], p[1]) for p in knitlib.machine_handler.get_available_ports()])
    return jsonify(port_dict)


@app.route('/v1/get_job_status/<job_id>')
@cross_origin()
def get_job_status(job_id):
    job_d = job_dict[job_id].get_job_public_dict()
    return jsonify(job_d)


@app.route('/v1/create_job/', methods=["POST"])
@cross_origin()
def create_knitting_job():
    """Creates a knitting job and inits the Machine plugin returning the job id."""
    plugin_id = request.form['plugin_id']
    port_str = request.form['port']
    plugin_class = knitlib.machine_handler.get_machine_plugin_by_id(plugin_id)
    job = KnittingJob(plugin_class, port_str, callbacks_dict={
        "blocking_user_action": emit_blocking_action_notification_dict,
        "progress": emit_progress,
        "message": emit_message_dict
    })
    job_string_id = str(job.id)
    job_dict[job_string_id] = job
    return jsonify({"job_id": job_string_id})


@app.route('/v1/init_job/<job_id>', methods=["POST"])
@cross_origin()
def init_job(job_id):
    job = job_dict.get(job_id)
    job.init_job()
    return get_job_status(job_id)


@app.route('/v1/configure_job/<job_id>', methods=["POST"])
@cross_origin()
def configure_knitting_job(job_id):
    """Configures job based on Knitpat file and binary Image."""
    knitpat_string = request.form['knitpat_dict']
    if request.files and 'file' in request.files:
        file = request.files['file']
        if file.filename is not '':
            filename = secure_filename(file.filename)
            filename_path = os.path.join(app.config['UPLOAD_FOLDER'])
            file.save(filename_path, filename)

    knitpat_dict = knitlib.knitpat.parse_ustring(knitpat_string)
    knitlib.knitpat.validate_dict(knitpat_dict)
    job = job_dict.get(job_id)
    job.configure_job(knitpat_dict)
    return get_job_status(job_id)


@app.route('/v1/knit_job/<job_id>', methods=["POST"])
@cross_origin()
def knit_job(job_id):
    """Starts the knitting process for Job ID."""
    job = job_dict.get(job_id)
    try:
        spawn(job.knit_job)
    except Exception as e:
        logging.error(e)
        return jsonify({"error": "Error on init of knitjob."})
    return get_job_status(job_id)


@sockets.route('/v1/knitting_socket')
def emit_socket(ws):
    break_emission = False
    while not break_emission:
        sleep(0.5)
        message = ws.receive()
        if message:
            logging.info("message recieved")
            logging.info(message)

        if len(msg_queue) >= 1:
            message = ws.receive()
            ms = msg_queue.pop()
            ws.send(ms["type"], ms["data"])
            logging.info("Emmited from queue: {}".format(ms))


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)

def emit_message_dict(msg, level):
    # emit('emit_message_dict', msg)
    msg_queue.append({"type": "emit_message_dict", "data": msg})
    logging.log("Queued emit_message_dict: {}".format(msg))


def emit_progress(percent, done, total):
    # emit("progress", {"percent": percent, "done": done, "total": total}, namespace="/knit")
    msg_queue.append({"type": "progress", "data": {"percent": percent, "done": done, "total": total}})
    logging.info("log info {0}, {1}, {2}".format(percent, done, total))


def emit_blocking_action_notification_dict(msg, level):
    logging.log("Blocking Action: {}".format(msg))
    time.sleep(10)
    pass


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
