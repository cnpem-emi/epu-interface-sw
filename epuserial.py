#!/usr/bin/python-sirius
from gpio import *

config()

def setBit(number, value, bit_index):
    mask = 1 << (bit_index)
    bit = number & mask

    if not(bit ^ (value << bit_index)):
        pass
    elif bit:
        number &= ~mask
    else:
        number |= mask

    return(number)

def read_start(driver):
    if driver in [0,1]:
        data = OCR1_read() & 1 << (0 + 4 * driver) 

    else:
        data = OCR2_read() & 1 << (0 + 4 * (driver % 2))
    return(data)

def read_enable(driver):
    if driver in [0,1]:
        data = OCR1_read() & 1 << (1 + 4 * driver)

    else:
        data = OCR2_read() & 1 << (1 + 4 * (driver % 2))

    return(data)

def read_halt(driver):
    if driver in [0,1]:
        data = OCR1_read() & 1 << (2 + 4 * driver)

    else:
        data = OCR2_read() & 1 << (2 + 4 * (driver % 2))

    return(data)

def write_start(driver, value):
    if driver in [0,1]:
        current = OCR1_read()
        OCR1_write(setBit(current, value, 0 + 4 * driver))

    else:
        current = OCR2_read()
        OCR2_write(setBit(current, value, 0 + 4 * driver % 2))

def write_enable(driver, value):
    if driver in [0,1]:
        current = OCR1_read()
        OCR1_write(setBit(current, value, 1 + 4 * driver))

    else:
        current = OCR2_read()
        OCR2_write(setBit(current, value, 1 + 4 * driver % 2))

def write_halt(driver, value):
    if driver in [0,1]:
        current = OCR1_read()
        OCR1_write(setBit(current, value, 2 + 4 * driver))

    else:
        current = OCR2_read()
        OCR2_write(setBit(current, value, 2 + 4 * driver % 2))
