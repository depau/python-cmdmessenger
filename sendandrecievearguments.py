#!/usr/bin/python
# sendandrecieve.py
# Author: Adrien Emery
# Make sure the you have the SendandRecieve example loaded onto the Arduino
import random
import sys
import serial
import time

from cmdmessenger import CmdMessenger
from serial.tools import list_ports
from serialmonitor import SerialMonitor

ON = 1
OFF = 0


class Commands(object):
  acknowledge = 0
  error = 1
  float_addition = 2
  float_addition_result = 3


class SendAndRecieveArguments(object):

    def __init__(self):
        # make sure this baudrate matches the baudrate on the Arduino
        self.running = False
        self.led_state = OFF
        self.baud = 115200

        try:
            # try to open the first available usb port
            self.port_name = self.list_usb_ports()[0][0]
            self.serial_port = serial.Serial(self.port_name, self.baud, timeout=0)
        except (serial.SerialException, IndexError):
            print 'Could not open serial port.'
            self.messenger = None
        else:
            print 'Serial port sucessfully opened.'
            self.messenger = CmdMessenger(self.serial_port)
            # attach callbacks
            self.messenger.attach(func=self.on_error, msgid=Commands.error)
            self.messenger.attach(func=self.on_float_addition_result,
                                  msgid=Commands.float_addition_result)

            # send a command that the arduino will acknowledge
            self.messenger.send_cmd(Commands.acknowledge)
            # Wait until the arduino sends and acknowledgement back
            self.messenger.wait_for_ack(ackid=Commands.acknowledge)
            print 'Arduino Ready'

    def list_usb_ports(self):
        """
        Use the grep generator to get a list of all USB ports.
        """
        ports =  [port for port in list_ports.grep('usb')]
        return ports

    def on_error(self, received_command, *args, **kwargs):
        """
        Callback function to handle errors
        """
        print 'Error:', args[0][0]

    def on_float_addition_result(self, received_command, *args, **kwargs):
        """
        Callback to handle the float addition response
        """
        print 'Addition Result:', args[0][0]
        print 'Subtraction Result:', args[0][1]
        print

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        t0 = time.clock()
        while self.running and self.messenger is not None:
            # Update the led state once every second
            if time.clock() - t0 > 2 :
                t0 = time.clock()
                a = random.randint(0, 10)
                b = random.randint(0, 10)
                print 'Sending: {}, {}'.format(a, b)
                self.messenger.send_cmd(Commands.float_addition, a, b)

            # Check to see if any data has been recieved
            self.messenger.feed_in_data()

if __name__ == '__main__':
    send_and_recieve_args = SendAndRecieveArguments()

    try:
        print 'Press Ctrl+C to exit...'
        print
        send_and_recieve_args.run()
    except KeyboardInterrupt:
        send_and_recieve_args.stop()
        print 'Exiting...'
