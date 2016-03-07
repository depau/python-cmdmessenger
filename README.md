# python-cmdmessenger
A CmdMessenger port for Python 3.*

## Installation ##
Put `cmdmessenger.py` into your project folder or in your python site packages.

You will also want to install `pyserial` for serial communcication with the Arduino (also the examples rely on it). To install PySerial run:

`$ pip install pyserial`

## Setup CmdMessenger on Arduino ###
To get setup on the Arduino see the setup instructions here:

https://github.com/thijse/Arduino-CmdMessenger

## Examples ##
The CmdMessenger library for Arduino comes with a bunch of great examples to get started and so far 3 of the examples on the PC side have been ported to python.

In the `examples` folder just run the python example with the corresponding example loaded on the the Arduino.

Currently there are examples for:

- Recieve
- SendAndRecieve
- SendAndReciveArguments
