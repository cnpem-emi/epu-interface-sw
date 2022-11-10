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
    if driver:
        data = start_count_SI

    else:
        data = start_count_AB
    return(data)

def read_enable(driver):
    data = OCR1_read() & 1 << (1 + 4 * driver)

    return(data)

def read_halt(driver):
    data = OCR1_read() & 1 << (2 + 4 * driver)

    return(data)

def write_start(driver):
    global start_count_AB
    global start_count_SI
    
    current = OCR1_read()

    OCR1_write(setBit(current, 1, 4 * driver))
    sleep(0.03)
    OCR1_write(setBit(current, 0, 4 * driver))

    if driver:
        start_count_SI += 1
    else:
        start_count_AB += 1

def write_enable(driver, value):
    current = OCR1_read()
    OCR1_write(setBit(current, value, 1 + 4 * driver))

def write_halt(driver, value):
    current = OCR1_read()
    OCR1_write(setBit(current, value, 2 + 4 * driver))

def reset(driver):
    current = OCR2_read()
    OCR2_write(setBit(current, 1, 4 * driver))
    sleep(1)
    OCR2_write(setBit(current, 0, 4 * driver))
