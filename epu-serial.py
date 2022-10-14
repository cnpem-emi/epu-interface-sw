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
        data = OCR1_read()

    else:
        data = OCR2_read()

    return(data[0 + 4*driver])

def read_enable(driver):
    if driver in [0,1]:
        data = OCR1_read()

    else:
        data = OCR2_read()

    return (data[1 + 4 * driver])

def read_halt(driver):
    if driver in [0,1]:
        data = OCR1_read()

    else:
        data = OCR2_read()

    return(data[2 + 4*driver])

def write_start(driver, value):
    if driver in [0,1]:
        current = OCR1_read()
        OCR1_write(setBit(current[0], value, 0 + 4 * driver))

    else:
        current = OCR1_read()
        OCR2_write(setBit(current[0], value, 0 + 4 * driver))

def write_enable(driver, value):
    if driver in [0,1]:
        current = OCR1_read()
        OCR1_write(setBit(current[0], value, 1 + 4 * driver))

    else:
        current = OCR1_read()
        OCR2_write(setBit(current[0], value, 1 + 4 * driver))

def write_halt(driver, value):
    if driver in [0,1]:
        current = OCR1_read()
        OCR1_write(setBit(current[0], value, 2 + 4 * driver))

    else:
        current = OCR1_read()
        OCR2_write(setBit(current[0], value, 2 + 4 * driver))