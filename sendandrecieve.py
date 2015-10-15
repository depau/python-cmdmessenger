#!/usr/bin/python
# sendandrecieve.py
# Author: Adrien Emery
# Make sure the you have the SendandRecieve example loaded onto the Arduino

import sys
import serial
import time

from cmdmessenger import CmdMessenger
from serial.tools import list_ports
from serialmonitor import SerialMonitor

ON = 1
OFF = 0

def list_usb_ports():
    """
    Use the grep generator to get a list of all USB ports.
    """
    ports =  [port for port in list_ports.grep('usb')]
    return ports

def on_unknown_command(self, received_command, *args, **kwargs):
    """
    Executes when an unknown command has been received.
    """
    print "Command without attached callback received"

def on_status(received_command, *args, **kwargs):
    """
    Callback function that prints the Arduino status to the console
    """
    print "Arduino status: ", args[0][0]
    # status = args[0][0]

class Commands(object):
    set_led = 0
    status = 1

if __name__ == '__main__':
    baud = 115200  # make sure this matches the baudrate on the Arduino

    try:
        # gets the first available USB port
        port_name = list_usb_ports()[0][0]
        serial_port = serial.Serial(port_name, baud, timeout=0)
    except (serial.SerialException, IndexError):
        print 'Could not open serial port.'
        sys.exit(1)
    else:
        print 'Serial port sucessfully opened.'
        messenger = CmdMessenger(serial_port)

        # attach callbacks
        messenger.attach(func=on_unknown_command)
        messenger.attach(func=on_status, msgid=Commands.status)

        # start the serial monitor thread
        # serial_monitor = SerialMonitor(serial_port, messenger)
        # serial_monitor.start()

    try:
        print 'Press Ctrl+C to exit...'
        # run a loop to turn on and off the LED once a second
        while True:
            messenger.send_cmd(Commands.set_led, ON)
            # wait for a response:
            messenger.feed_in_data()
            messenger.send_cmd(Commands.set_led, OFF)
            messenger.feed_in_data()
    except KeyboardInterrupt:
        # kill the serial monitor thread
        # serial_monitor.stop()
        print 'Exiting...'
