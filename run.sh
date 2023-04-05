#!/bin/bash
# -*- coding: utf-8 -*-

echo "Exporting SPI pins"

./configpin.sh

echo "Setting RS485 interface"
socat TCP-LISTEN:5002,reuseaddr,fork,nodelay FILE:/dev/ttyUSB0,b19200 &

echo "Starting socket"

pushd scripts
    ./epusocket.py
popd
