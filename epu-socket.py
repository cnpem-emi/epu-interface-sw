#!/usr/bin/python-sirius

import time
import socket
import logging
from threading import Thread

# BSMP Variable IDs

HALT_CH_A =   0x10
START_CH_A =  0x20
ENABLE_CH_A = 0x30

HALT_CH_B =   0x11
START_CH_B =  0x21
ENABLE_CH_B = 0x31

HALT_CH_S =   0x12
START_CH_S =  0x22
ENABLE_CH_S = 0x32

HALT_CH_I =   0x13
START_CH_I =  0x23
ENABLE_CH_I = 0x33

def verifyChecksum(list_values):
    counter = 0
    i = 0
    while(i < len(list_values)):
        counter += list_values[i]
        i += 1
    counter = (counter & 0xFF)

    return(counter)

# Thead to send and receive values on demand
class Communication(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.port = port
        self.ch = {0:"A", 1:"B", 2:"S", 3:"I"}

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
                    logger.info("Waiting for connection.\n")
                    con, client_info = self.tcp.accept()

                    # New connection
                    logger.info(f"Connection accepted from {client_info[0]}:{str(client_info[1])}.\n")

                    while (True):
                        # Get message
                        message = [ord(i) for i in con.recv(100).decode('latin-1')]
                        if(message):
                            if (verifyChecksum(message) == 0):
                                # Variable Read
                                if message[1] == 0x10:
                                    pass        #Nothing to read

                                elif message[1] == 0x20:
                                    if message[4] in [HALT_CH_A, HALT_CH_B, HALT_CH_S, HALT_CH_I]:
                                        logger.info(f"HALT COMMAND RECEIVED - Channel {self.ch[message[4]%0x10]}")
                                        #CALL_FUNC(message[4] % 0x10)

                                    elif message[4] in [START_CH_A, START_CH_B, START_CH_S, START_CH_I]:
                                        logger.info(f"START COMMAND RECEIVED - Channel {self.ch[message[4] % 0x20]}")
                                        #CALL_FUNC(message[4] % 0x20)

                                    elif message[4] in [ENABLE_CH_A, ENABLE_CH_B, ENABLE_CH_S, ENABLE_CH_I]:
                                        logger.info(f"ENABLE COMMAND RECEIVED - Channel {self.ch[message[4] % 0x30]}")
                                        #CALL_FUNC(message[4] % 0x30)

                                    else:
                                        logger.error("Command not supported")
                                else:
                                    logger.warning("First byte must be 0x20")

                            else:
                                logger.warning(f"Unknown message: {message}\n, verify checksum.")
                                continue

                        else:
                            # Disconnection
                            logger.info(f"Client {client_info[0]}:{str(client_info[1])} disconected\n")
                            break

            except Exception:
                self.tcp.close()
                logger.warning("Connection problem. TCP/IP server was closed.\n")
                time.sleep(5)

# --------------------- MAIN LOOP ---------------------
# -------------------- starts here --------------------

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s [%(levelname)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
global logger
logger = logging.getLogger()

# Socket thread
net = Communication(5000)
net.daemon = True
net.start()

while(True):
    time.sleep(10)
