#!/bin/bash
# -*- coding: utf-8 -*-

echo "Exporting SPI pins"

./configpin.sh

echo "Setting RS485 interface"

echo "Starting socket"

pushd scripts
    ./epusocket.py
popd