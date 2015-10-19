#!/usr/bin/python
# receive.py
# Author: Adrien Emery
# Make sure the you have the Receive example loaded onto the Arduino

import sys
import serial
import time

from cmdmessenger import CmdMessenger
from serial.tools import list_ports


ON = 1
OFF = 0


class Receive(object):

    def __init__(self):
        self.running = False
        self.led_state = OFF
        self.commands = ['set_led']
        # make sure this baudrate matches the baudrate on the Arduino
        self.baud = 115200

        try:
            # gets the first available USB port
            self.port_name = self.list_usb_ports()[0][0]
            self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0)
        except (serial.SerialException, IndexError):
            raise SystemExit('Could not open serial port.')
        else:
            print 'Serial port sucessfully opened.'
            self.messenger = CmdMessenger(self.serial_port)

    def list_usb_ports(self):
        """Use the grep generator to get a list of all USB ports.
        """
        ports =  [port for port in list_ports.grep('usb')]
        return ports

    def stop(self):
        """Stops the main run loop
        """
        self.running = False

    def run(self):
        """Main loop to send data to the Arduino
        """
        self.running = True
        timeout = 1
        t0 = time.time()
        while self.running:
            # Update the led state once every second
            if time.time() - t0 > timeout:
                t0 = time.time()
                if self.led_state == ON:
                    self.messenger.send_cmd(self.commands.index('set_led'), OFF)
                    self.led_state = OFF
                else:
                    self.messenger.send_cmd(self.commands.index('set_led'), ON)
                    self.led_state = ON


if __name__ == '__main__':
    receive = Receive()

    try:
        print 'Press Ctrl+C to exit...'
        receive.run()
    except KeyboardInterrupt:
        receive.stop()
        print 'Exiting...'
