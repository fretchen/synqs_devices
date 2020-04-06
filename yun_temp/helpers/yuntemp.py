""" Simulate the YunTemp.

This is an extremely simple server that might be used for testing the arduino webserver interface.
It is based on flask. So before running it, you should run a
::

    pip install flask, flask_basicauth

If you want to run it you can just start it through:
::

    python yuntemp.py

This will open a test server on 127.0.0.1:5001. You can then adress it with the requests package.
::

    > r = requests.get('http://127.0.0.1:5001/arduino/read/all/')
    > r.text
    'setpoint, input, error, output, G, tauI, tauD <br />0,719,0,0,0,0,0'
"""

import random
from flask import Flask  # , request, jsonify
from flask_basicauth import BasicAuth

APP = Flask(__name__)


### uncomment the next few lines to test the authentification on the Yun
APP.config["BASIC_AUTH_USERNAME"] = "john"
APP.config["BASIC_AUTH_PASSWORD"] = "matrix"
APP.config["BASIC_AUTH_FORCE"] = True

BASIC_AUTH = BasicAuth(APP)

SETPOINT = 0
GAIN = 0
TAU_I = 0
ERR = 0
CONTROL = 0
TAU_D = 0


@APP.route("/arduino/read/all/")
def get_temp():
    """Read out all properties from the arduino.

    Calculates back some random value and gives back whatever was set.

    Returns:
        a text string.
    """
    meas = random.randint(700, 800)
    global SETPOINT, GAIN, TAU_I, ERR, CONTROL, TAU_D
    print(SETPOINT)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(SETPOINT) + "," + str(meas) + "," + str(ERR) + "," + str(CONTROL)
    ard_str = ard_str + "," + str(GAIN) + "," + str(TAU_I) + "," + str(TAU_D)

    return first_line + ard_str


@APP.route("/arduino/write/setpoint/<float:n_val>/")
def set_setpoint(n_val):
    """Set the setpoint of the temp control.

    Args:
        n_val: The setpoint that is chosen.

    Returns:
        a text string.
    """
    global SETPOINT, GAIN, TAU_I, ERR, CONTROL, TAU_D
    SETPOINT = n_val
    print(SETPOINT)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(SETPOINT) + "," + str(meas) + "," + str(ERR) + "," + str(CONTROL)
    ard_str = ard_str + "," + str(GAIN) + "," + str(TAU_I) + "," + str(TAU_D)

    return first_line + ard_str


@APP.route("/arduino/write/integral/<float:n_val>/")
def set_integral(n_val):
    """Set the integrator of the temp control.

    Args:
        n_val: The integral value that is chosen.

    Returns:
        a text string.
    """
    global SETPOINT, GAIN, TAU_I, ERR, CONTROL, TAU_D
    TAU_I = n_val
    print(TAU_I)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(SETPOINT) + "," + str(meas) + "," + str(ERR) + "," + str(CONTROL)
    ard_str = ard_str + "," + str(GAIN) + "," + str(TAU_I) + "," + str(TAU_D)

    return first_line + ard_str


@APP.route("/arduino/write/differential/<float:n_val>/")
def set_differential(n_val):
    """Set the D of the temp control.

    Args:
        n_val: The D value that is chosen.

    Returns:
        a text string.
    """
    global SETPOINT, GAIN, TAU_I, ERR, CONTROL, TAU_D
    TAU_D = n_val
    print(TAU_D)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(SETPOINT) + "," + str(meas) + "," + str(ERR) + "," + str(CONTROL)
    ard_str = ard_str + "," + str(GAIN) + "," + str(TAU_I) + "," + str(TAU_D)

    return first_line + ard_str


@APP.route("/arduino/write/gain/<float:n_val>/")
def set_gain(n_val):
    """Set the proportional of the temp control.

    Args:
        n_val: The P value that is chosen.

    Returns:
        a text string.
    """
    global SETPOINT, GAIN, TAU_I, ERR, CONTROL, TAU_D
    GAIN = n_val
    print(GAIN)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(SETPOINT) + "," + str(meas) + "," + str(ERR) + "," + str(CONTROL)
    ard_str = ard_str + "," + str(GAIN) + "," + str(TAU_I) + "," + str(TAU_D)

    return first_line + ard_str


if __name__ == "__main__":
    APP.run(port=5001, debug=True)
