#!/usr/bin/python-sirius
from Adafruit_BBIO.SPI import SPI
#-------------------------------------------------------
# initialize the bus and device /dev/spidev1.0
spi = SPI(0,0)
#-------------------------------------------------------
# port A: all INPUTS
# port B: 3 INPUTS and 5 OUTPUTS
# port C: all tri-state
# port D: all tri-state
#-------------------------------------------------------
'''
!!! IMPORTANT INFORMATION !!!
1. For sending data to the register, the SPI mode should be set to 0
2. For receiving data from the register, the SPI mode should be set to 1
3. Yes, I know.. this is bizarre!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

Adapted in oct/22 from https://github.com/lnls-sirius/SPIxCONV/blob/master/software/scripts/gpio.py

========================================================
 SPI Write
========================================================
SI:		|1|0|0|A3|A2|A1|A0|X|
SO: 						|D7|D6|D5|D4|D3|D2|D1|D0|
========================================================
 SPI Read
========================================================
SI:		|0|0|0|A3|A2|A1|A0|X|D7|D6|D5|D4|D3|D2|D1|D0|
========================================================
Command Byte	Register	 R/W		Default values
-------------  ---------   --------   ------------------
	0x00		GSR1		R-only			0xXX
	0x01		GSR2		R-only			0xXX
	0x02		OCR1		 R/W			0xFF
	0x03		OCR2		 R/W			0xFF
	0x06		GCR1		 R/W			0xFF
	0x07		GCR2		 R/W			0xFF
	0x0C		TSCR1		 R/W			0x00
	0x0D		TSCR2		 R/W			0x00
========================================================
'''
#=======================================================
# initial GPIO configuration
#=======================================================
def config():
    '''
    input parameters:
        - board: none
    output parameters:
        - none
    ----------------------------
    description:
        this function configures the digital pins direction:
            Port A:
            	b0, b1, b2, b4, b5 and b6: Output
            	b3 and b7: Input
            Port B:
            	b8, b9, b10, b12, b13 and b14: Output
            	b11 and b15: Input
    ----------------------------
    GCR:
        0: configures that pin as OUTPUT.
        1: configures that pin as INPUT.
    TSCR:
        0: DISABLE three-state mode.
        1: ENABLE three-state mode.
    '''

    # enable tri-state mode in ports A and B
    TSCR1_write(0xFF)
    TSCR2_write(0xFF)
    # set port A inputs/outputs
    GCR1_write(0x88)				# 10001000
    # set port B inputs/outputs
    GCR2_write(0x88)				# 10001000
    # set all initial outputs value low
    OCR1_write(0x00)
    OCR2_write(0x00)
    # disable tri-state mode
    TSCR1_write(0x00)
    TSCR2_write(0x00)
#=======================================================
# initial GPIO configuration
#=======================================================
    '''
    input parameters:
        - none
    output parameters:
        - none
    ----------------------------
    description:
        this function was created for debug only
        it reads all the main registers
    ----------------------------
    '''
def rr():
    print("GSR1 = ", str(GSR1()))
    print("GSR2 = ", str(GSR2()), "\n")
    print("GCR1 = ", str(GCR1_read()))
    print("GCR2 = ", str(GCR2_read()), "\n")
    print("OCR1 = ", str(OCR1_read()))
    print("OCR2 = ", str(OCR2_read()), "\n")
    print("TSCR1 = " + str(TSCR1_read()))
    print("TSCR2 = " + str(TSCR2_read()), "\n")

#=======================================================
# GPIO State Register 1 and 2 (GSR1 and GSR2)
#=======================================================
# reading digital value in P0-P7
def GSR1():
	command = (1 << 7) or (0x00 << 1)
	spi.writebytes([command])
	data = spi.readbytes(1)
	return(data[0])

# reading digital value in P8-P15
def GSR2():
	command = (1 << 7) ^ (0x01 << 1)
	spi.writebytes([command])
	data = spi.readbytes(1)
	return(data[0])
#=======================================================
# Output Control Register 1 and 2 (OCR1 and OCR2)
#=======================================================
# writing digital value in P0-P7
def OCR1_write(value):
    spi.mode = 0
    command = 0x02 << 1
    spi.writebytes([command,value])
    spi.mode = 1
#-------------------------------------------------------
# writing digital value in P8-P15
def OCR2_write(value):
    spi.mode = 0
    command = 0x03 << 1
    spi.writebytes([command,value])
    spi.mode = 1
#-------------------------------------------------------
# reading last value put in P0-P7
def OCR1_read():
	spi.mode = 0
	command = (1 << 7) ^ (0x02 << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data[0])
#-------------------------------------------------------
# reading last value put in P8-P15
def OCR2_read():
	spi.mode = 0
	command = (1 << 7) ^ (0x03 << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data[0])
#=======================================================
# GPIO Configuration Register 1 and 2 (GCR1 and GCR2)
#=======================================================
'''
if bit = 0:	OUTPUT
if bit = 1:	INPUT
'''
# configuring P0-P7 (Port A or C) as input or outputs
def GCR1_write(value):
	spi.mode = 0
	command = 0x06 << 1
	spi.writebytes([command,value])
	spi.mode = 1
#-------------------------------------------------------
# configuring P8-P15 (Port B or D) as input or outputs
def GCR2_write(value):
	spi.mode = 0
	command = 0x07 << 1
	spi.writebytes([command,value])
	spi.mode = 1
#-------------------------------------------------------
# reading GPIO configuration of P0-P7 (Port A or C)
def GCR1_read():
	spi.mode = 0
	command = (1 << 7) ^ (0x06 << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data[0])
#-------------------------------------------------------
# reading GPIO configuration of P8-P15 (Port B or D)
def GCR2_read():
	spi.mode = 0
	command = (1 << 7) ^ (0x07 << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data[0])
#=======================================================
# Output Three-State Control Register 1 and 2 (TSCR1 and TSCR2)
#=======================================================
'''
if bit = 0:	DISABLE three-state mode
if bit = 1:	 ENABLE three-state mode
'''
# enabling/disabling P0-P7 (Port A or C) three-state mode
def TSCR1_write(value):
	spi.mode = 0
	command = (0x0C << 1)
	spi.writebytes([command, value])
	spi.mode = 1
#-------------------------------------------------------
# enabling/disabling P8-P15 (Port B or D) three-state mode
def TSCR2_write(value):
	spi.mode = 0
	command = (0x0D << 1)
	spi.writebytes([command, value])
	spi.mode = 1
#-------------------------------------------------------
# reading P0-P7 (Port A or C) three-state mode
def TSCR1_read():
	spi.mode = 0
	command = (1 << 7) ^ (0x0C << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data[0])
#-------------------------------------------------------
# reading P8-P15 (Port B or D) three-state mode
def TSCR2_read():
	spi.mode = 0
	command = (1 << 7) ^ (0x0D << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data[0])
#=======================================================
# write into a specific register
def write_register(command, value):
	spi.mode = 0
	command = command << 1
	spi.writebytes([command,value])
	spi.mode = 1
#=======================================================
# read a specific register
def read_register(command):
	spi.mode = 0
	command = (1 << 7) ^ (command << 1)
	spi.writebytes([command])
	spi.mode = 1
	data = spi.readbytes(1)
	return(data)
#=======================================================