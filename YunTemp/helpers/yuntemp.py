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

from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
import random

app = Flask(__name__)


### uncomment the next few lines to test the authentification on the Yun
# app.config['BASIC_AUTH_USERNAME'] = 'john'
# app.config['BASIC_AUTH_PASSWORD'] = 'matrix'
# app.config['BASIC_AUTH_FORCE'] = True

# basic_auth = BasicAuth(app)

setpoint = 0
gain = 0
tauI = 0
err = 0
control = 0
tauD = 0


@app.route("/arduino/read/all/")
def get_temp():
    """Read out all properties from the arduino.

    Calculates back some random value and gives back whatever was set.

    Returns:
        a text string.
    """
    meas = random.randint(700, 800)
    global setpoint, gain, tauI, err, control, tauD
    print(setpoint)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(setpoint) + "," + str(meas) + "," + str(err) + "," + str(control)
    ard_str = ard_str + "," + str(gain) + "," + str(tauI) + "," + str(tauD)

    return first_line + ard_str


@app.route("/arduino/write/setpoint/<float:n_val>/")
def set_setpoint(n_val):
    """Set the setpoint of the temp control.

    Args:
        n_val: The setpoint that is chosen.

    Returns:
        a text string.
    """
    global setpoint, gain, tauI, err, control, tauD
    setpoint = n_val
    print(setpoint)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(setpoint) + "," + str(meas) + "," + str(err) + "," + str(control)
    ard_str = ard_str + "," + str(gain) + "," + str(tauI) + "," + str(tauD)

    return first_line + ard_str


@app.route("/arduino/write/integral/<float:n_val>/")
def set_integral(n_val):
    """Set the integrator of the temp control.

    Args:
        n_val: The integral value that is chosen.

    Returns:
        a text string.
    """
    global setpoint, gain, tauI, err, control, tauD
    tauI = n_val
    print(tauI)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(setpoint) + "," + str(meas) + "," + str(err) + "," + str(control)
    ard_str = ard_str + "," + str(gain) + "," + str(tauI) + "," + str(tauD)

    return first_line + ard_str


@app.route("/arduino/write/differential/<float:n_val>/")
def set_differential(n_val):
    """Set the D of the temp control.

    Args:
        n_val: The D value that is chosen.

    Returns:
        a text string.
    """
    global setpoint, gain, tauI, err, control, tauD
    tauD = n_val
    print(tauD)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(setpoint) + "," + str(meas) + "," + str(err) + "," + str(control)
    ard_str = ard_str + "," + str(gain) + "," + str(tauI) + "," + str(tauD)

    return first_line + ard_str


@app.route("/arduino/write/gain/<float:n_val>/")
def set_gain(n_val):
    """Set the proportional of the temp control.

    Args:
        n_val: The P value that is chosen.

    Returns:
        a text string.
    """
    global setpoint, gain, tauI, err, control, tauD
    gain = n_val
    print(gain)
    meas = random.randint(700, 800)
    first_line = "setpoint, input, error, output, G, tauI, tauD <br />"
    ard_str = str(setpoint) + "," + str(meas) + "," + str(err) + "," + str(control)
    ard_str = ard_str + "," + str(gain) + "," + str(tauI) + "," + str(tauD)

    return first_line + ard_str


if __name__ == "__main__":
    app.run(port=5001, debug=True)
