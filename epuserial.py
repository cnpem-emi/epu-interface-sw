#!/usr/bin/python-sirius
from gpio import *
from time import sleep

config()
start_count_AB = 0
start_count_SI = 0

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
    if (driver == 0):
        data = start_count_AB

    else:
        data = start_count_SI
    return(data)

def read_enable(driver):
    if (driver == 0):
        data = OCR1_read() & 1 << (1 + 4 * driver)

    else:
        data = OCR2_read() & 1 << (1 + 4 * (driver % 2))

    return(data)

def read_halt(driver):
    if (driver == 0):
        data = OCR1_read() & 1 << (2 + 4 * driver)

    else:
        data = OCR2_read() & 1 << (2 + 4 * (driver % 2))

    return(data)

def write_start(driver):
    if (driver == 0):
        current = OCR1_read()

        OCR1_write(setBit(current, 1, 0 + 4 * driver))
        sleep(0.03)
        OCR1_write(setBit(current, 0, 0 + 4 * driver))

        start_count_AB += 1

    else:
        current = OCR2_read()

        OCR2_write(setBit(current, 1, 0 + 4 * (driver % 2)))
        sleep(0.03)
        OCR2_write(setBit(current, 0, 0 + 4 * (driver % 2)))

        start_count_SI += 1

def write_enable(driver, value):
    if (driver == 0):
        current = OCR1_read()
        OCR1_write(setBit(current, value, 1 + 4 * driver))

    else:
        current = OCR2_read()
        OCR2_write(setBit(current, value, 1 + 4 * (driver % 2)))

def write_halt(driver, value):
    if (driver == 0):
        current = OCR1_read()
        OCR1_write(setBit(current, value, 2 + 4 * driver))

    else:
        current = OCR2_read()
        OCR2_write(setBit(current, value, 2 + 4 * (driver % 2)))
