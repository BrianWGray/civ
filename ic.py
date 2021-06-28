#! /usr/bin/python3
#
# Quick and Dirty PoC
# Turn Radio on/off
# @BrianWGray
# 06.28.2021

#Import libraries we'll need to use
import sys
import struct
import serial # pip3 install pyserial

# Below are variables you need to change to match your radio address etc.
RADIO_ADDRESS = "0x94" #address of the radio
BAUDRATE = 19200  #change to match your radio
BUFF_LENGTH = 150 # different baudrates have different recommended length
SERIALPORT = "COM3"  # Serial port of your radios serial interface.

BUFF = ["0xFE"]
COMMAND = ["0x18"]
DATA = ["0x01"]

PRE_BUFF = BUFF * BUFF_LENGTH
PREAMBLE = ["0xFE", "0xFE", RADIO_ADDRESS, "0xE0"]
POSTAMBLE = ["0xfd"]

class RadioCmd:
    '''radio command object to manipulate'''

    def message(self, cmd, cmd_data):
        '''Define the command send in hex bytes.'''

        self.msg = []

        self.cmd = cmd
        self.cmd_data = cmd_data

        # Assemble message
        self.msg.extend(PRE_BUFF)
        self.msg.extend(PREAMBLE)
        self.msg.extend(self.cmd)
        self.msg.extend(self.cmd_data)
        self.msg.extend(POSTAMBLE)
        return self.msg

    def send(self):
        '''Send message over serial'''
        #set and send message
        ser = serial.Serial(SERIALPORT, BAUDRATE)

        msg_length = len(self.msg)
        count = 0
        while(count < msg_length):
            send_data = int(bytes(self.msg[count], 'UTF-8'), 16)
            ser.write(struct.pack('>B', send_data))
            count = count +1

        ser.close()

def main(argv):
    on  = ["0x01"]
    off = ["0x00"]

    if(argv == "on"):
        data = on
    else:
        data = off

    radio = RadioCmd()

    #(cmd = ["0x18"], cmd_data = ["0x01"]) Radio power state on
    radio.message(COMMAND, DATA)
    radio.send()

if __name__ == "__main__":
    main(sys.argv[1])
