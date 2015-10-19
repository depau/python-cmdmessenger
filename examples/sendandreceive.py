#!/usr/bin/python
# sendandreceive.py
# Author: Adrien Emery
# Make sure the you have the SendAndReceive example loaded onto the Arduino

import sys
import serial
import time

from cmdmessenger import CmdMessenger
from serial.tools import list_ports

ON = 1
OFF = 0


class SendAndReceive(object):

    def __init__(self):
        # make sure this baudrate matches the baudrate on the Arduino
        self.running = False
        self.led_state = OFF
        self.baud = 115200
        self.commands = ['set_led',
                         'status',
                         ]

        try:
            # gets the first available USB port
            self.port_name = self.list_usb_ports()[0][0]
            self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0)
        except (serial.SerialException, IndexError):
            raise SystemExit('Could not open serial port.')
        else:
            print 'Serial port sucessfully opened.'
            self.messenger = CmdMessenger(self.serial_port)
            # attach callbacks
            self.messenger.attach(func=self.on_unknown_command)
            self.messenger.attach(func=self.on_status, msgid=self.commands.index('status'))

    def list_usb_ports(self):
        """Use the grep generator to get a list of all USB ports.
        """
        ports =  [port for port in list_ports.grep('usb')]
        return ports

    def on_unknown_command(self, received_command, *args, **kwargs):
        """Handle when an unknown command has been received.
        """
        print "Command without attached callback received"

    def on_status(self, received_command, *args, **kwargs):
        """Callback function that prints the Arduino status to the console
        """
        print "Status: ",  args[0][0]

    def stop(self):
        """ Stops the main run loop
        """
        self.running = False

    def run(self):
        """Main loop to send and receive data from the Arduino
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

            # Check to see if any data has been received
            self.messenger.feed_in_data()

if __name__ == '__main__':
    send_and_receive = SendAndReceive()

    try:
        print 'Press Ctrl+C to exit...'
        send_and_receive.run()
    except KeyboardInterrupt:
        send_and_receive.stop()
        print 'Exiting...'
