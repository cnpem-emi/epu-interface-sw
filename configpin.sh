#!/bin/bash

#==========================
# SPI pins exported
#==========================

echo "Exporting ..."

config-pin P9_17 spi_cs         # CS
config-pin P9_21 spi            # DO
config-pin P9_18 spi            # DI
config-pin P9_22 spi_sclk       # CLK

config-pin P9_14 gpio           # DS
