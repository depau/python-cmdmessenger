from threading import Thread
import serial


class SerialMonitor(Thread):

    def __init__(self, serial_object, cmd_messenger):
        super(SerialMonitor, self).__init__()
        self.is_running = False
        self.serial_object = serial_object
        self.cmd_messenger = cmd_messenger

    def stop(self):
        self.is_running = False
        print 'Stopping serial monitor'

    def run(self):
        self.is_running = True
        while(self.is_running):
            num_bytes_waiting = self.serial_object.inWaiting()
            if num_bytes_waiting > 0:
                data = self.cmd_messenger.feed_in_data(num_bytes_waiting)
                # print 'raw data:', data
                # self.cmd_messenger.feed_in_string(data)
