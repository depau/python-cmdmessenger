#!/usr/bin/python
# recieve.py
# Author: Adrien Emery
# Make sure the you have the Recieve example loaded onto the Arduino

import sys
import serial
import time

from cmdmessenger import CmdMessenger
from serial.tools import list_ports

ON = 1
OFF = 0


class Commands(object):
    set_led = 0
    status = 1


class Recieve(object):

    def __init__(self):
        # make sure this baudrate matches the baudrate on the Arduino
        self.running = False
        self.led_state = OFF
        self.baud = 115200

        try:
            # gets the first available USB port
            self.port_name = self.list_usb_ports()[0][0]
            self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0)
        except (serial.SerialException, IndexError):
            print 'Could not open serial port.'
            self.messenger = None
        else:
            print 'Serial port sucessfully opened.'
            self.messenger = CmdMessenger(self.serial_port)

    def list_usb_ports(self):
        """
        Use the grep generator to get a list of all USB ports.
        """
        ports =  [port for port in list_ports.grep('usb')]
        return ports

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        t0 = time.clock()
        while self.running:
            # Update the led state once every second
            if time.clock() - t0 > 1:
                t0 = time.clock()
                if self.led_state == ON:
                    self.messenger.send_cmd(Commands.set_led, OFF)
                    self.led_state = OFF
                else:
                    self.messenger.send_cmd(Commands.set_led, ON)
                    self.led_state = ON

if __name__ == '__main__':
    recieve = Recieve()

    try:
        print 'Press Ctrl+C to exit...'
        recieve.run()
    except KeyboardInterrupt:
        recieve.stop()
        print 'Exiting...'
