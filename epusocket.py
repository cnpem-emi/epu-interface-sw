#!/usr/bin/python-sirius

import time
import socket
import struct
import logging
from epuserial import *
from threading import Thread
from logging.handlers import RotatingFileHandler

# BSMP Variable IDs

HALT_CH_AB =   0x10
START_CH_AB =  0x20
ENABLE_CH_AB = 0x30

HALT_CH_SI =   0x11
START_CH_SI =  0x21
ENABLE_CH_SI = 0x31

RESET_CH_AB =  0x40
RESET_CH_SI =  0x41

# Status code

BUSY =          0xe8
READ_OK =       0x11
WRITE_OK =      0xe0
INVALID_ID =    0xe3
BAD_FORMATTED = 0xe1

def sendVariable(statusID, variableID = 0x00, value = 0x00, size = 0):
    send_message = [0x00, statusID] + [c for c in struct.pack("!h", size + 1)] + [variableID]
    if size == 1:
        send_message = send_message + [value]
    elif size == 2:
        send_message = send_message + [c for c in struct.pack("!h", value)]
    elif size == 4:
        send_message = send_message + [c for c in struct.pack("!I", value)]
    return("".join(map(chr, includeChecksum(send_message))))

def includeChecksum(list_values):
    counter = 0
    i = 0
    while (i < len(list_values)):
        counter += list_values[i]
        i += 1
    counter = (counter & 0xFF)
    counter = (256 - counter) & 0xFF
    return(list_values + [counter])

def verifyChecksum(list_values):
    counter = 0
    for data in list_values:
        counter += data
       
    counter = (counter & 255)
    return(counter)

# Thead to send and receive values on demand
class Communication(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.port = port
        self.ch = {0:"AB", 1:"SI"}

    def run(self):
        while True:
            try:
                # TCP/IP socket initialization
                self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.tcp.bind(("", self.port))
                self.tcp.listen(1)

                logger.info("----- EPU Socket -----")
                logger.info(f"TCP/IP Server on port {str(self.port)} started.\n")

                while(True):
                    logger.info("Waiting for connection ...\n")
                    con, client_info = self.tcp.accept()

                    # New connection
                    logger.info(f"Connection accepted from {client_info[0]}:{str(client_info[1])}.\n")

                    while (True):
                        # Get message
                        message = [ord(i) for i in con.recv(100).decode()]
                        if(message):
                            if (verifyChecksum(message) == 0):
                                # Variable Read
                                if message[1] == 0x10:
                                    if message[4] in [HALT_CH_AB, HALT_CH_SI]:
                                        logger.info(f"HALT COMMAND READ - Channels {self.ch[message[4] % 0x10]}")
                                        con.send(sendVariable(READ_OK, message[4], read_halt(message[4] % 0x10), 1).encode('latin-1'))

                                    elif message[4] in [START_CH_AB, START_CH_SI]:
                                        logger.info(f"START COMMAND READ - Channels {self.ch[message[4] % 0x20]}")
                                        con.send(sendVariable(READ_OK, message[4], read_start(message[4] % 0x20), 1).encode('latin-1'))

                                    elif message[4] in [ENABLE_CH_AB, ENABLE_CH_SI]:
                                        logger.info(f"ENABLE COMMAND READ - Channels {self.ch[message[4] % 0x30]}")
                                        con.send(sendVariable(READ_OK, message[4], read_enable(message[4] % 0x30), 1).encode('latin-1'))

                                    else:
                                        con.send(sendVariable(INVALID_ID).encode('latin-1'))
                                        logger.error("Command not supported")

                                # Variable Write
                                elif message[1] == 0x20:
                                    try:
                                        if message[4] in [HALT_CH_AB, HALT_CH_SI]:
                                            logger.info(f"HALT COMMAND RECEIVED - Channels {self.ch[message[4]%0x10]} set to {message[5] and 1}")
                                            write_halt(message[4] % 0x10, message[5] and 1)
                                        
                                        elif message[4] in [START_CH_AB, START_CH_SI]:
                                            logger.info(f"START COMMAND RECEIVED - Channels {self.ch[message[4] % 0x20]} set to {message[5] and 1}")
                                            write_start(message[4] % 0x20)
                                        
                                        elif message[4] in [ENABLE_CH_AB, ENABLE_CH_SI]:
                                            logger.info(f"ENABLE COMMAND RECEIVED - Channels {self.ch[message[4] % 0x30]} set to {message[5] and 1}")
                                            write_enable(message[4] % 0x30, message[5] and 1)
                                     
                                        elif message[4] in [RESET_CH_AB, RESET_CH_SI]:
                                            logger.info(f"RESET COMMAND RECEIVED - Channels {self.ch[message[4] % 0x40]}")
                                            reset(message[4] % 0x40)
                                    
                                        else:
                                            con.send(sendVariable(INVALID_ID).encode('latin-1'))
                                            logger.error("Command not supported")
                                    
                                    except Exception as e:
                                        logger.warning(f"An error occurred during the write command: {e}")
                                        con.send(sendVariable(BUSY).encode('latin-1'))
                                    else:
                                        con.send(sendVariable(WRITE_OK).encode('latin-1'))
                                                       
                                else:
                                    logger.warning("Second byte must be 0x10 or 0x20")
                                    con.send(sendVariable(BAD_FORMATTED).encode('latin-1'))

                            else:
                                logger.warning(f"Unknown message: {message}, verify checksum.\n")
                                con.send(sendVariable(BAD_FORMATTED).encode('latin-1'))
                                continue

                        else:
                            # Disconnection
                            logger.info(f"Client {client_info[0]}:{str(client_info[1])} disconected.\n")
                            break

            except Exception as e:
                self.tcp.close()
                logger.warning(f"Connection problem: {e}. \nTCP/IP server was closed.\n")
                time.sleep(5)

# --------------------- MAIN LOOP ---------------------
# -------------------- starts here --------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s [%(levelname)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
global logger
logger = logging.getLogger()

# Socket thread
net = Communication(5050)
net.daemon = True
net.start()

while(True):
    time.sleep(10)
