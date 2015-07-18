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

from flask import Flask, jsonify
import knitlib

app = Flask(__name__)
# A reference for creating new RESTful endpoints:
# http://blog.luisrei.com/articles/flaskrest.html


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/v1/get_machine_plugins')
def get_machine_plugins():
    return jsonify(knitlib.machine_handler.get_active_machine_plugins_names())


@app.route('/v1/get_ports')
def get_ports():
    port_dict = dict([(p[0], p[1]) for p in knitlib.machine_handler.get_available_ports()])
    return jsonify(port_dict)


if __name__ == '__main__':
    app.run(debug=True)
