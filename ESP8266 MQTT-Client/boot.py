﻿#!/usr/bin/env micropython
'''
Tufts University CEEO Fetlab (PTC), Summer 2021
boot.py
By: Sawyer Bailey Paccione
Description: Once saved to the ESP this file runs as soon as the board is
             provided power.
Purpose:     This program connects the ESP board to WiFi and defines important
             configuration files.
'''

import utime
from umqtt.simple import MQTTClient  # Pre-built into ESP boards
import ubinascii  # Convert Ascii to Hex
import machine  # Controlling Pins and status of the board
import network  # Connect the board to WiFi
import esp, uos, gc, sys

# from sensitive_data import sensitive_data  # Info for the CONFIGs

esp.osdebug(None)  # turn off vendor O/S debugging messages
gc.collect()  # Run a garbage collection.

uart = machine.UART(0, 115200, timeout=50)  # init uart with given parameters
uos.dupterm(uart, 1)  # Attach the REPL to UART0

WIFI_CONFIG = {
    # Configuration Details for the WIFI the Edge Server is on
    "SSID": "<NAME OF WIFI>",
    "PASS": "<PASSWORD TO WIFI>"
}

MQTT_CONFIG = {
    # Configuration details of the MQTT Broker
    "MQTT_BROKER": "<ADDRESS OF MQTT BROKER>",
    "USER": "",
    "PASS": "",
    "PORT": 1883,
    "PUB_TOPIC1": b'hub_data',
    "PUB_TOPIC2": b'',
    "SUB_TOPIC1": b'commands',
    "SUB_TOPIC2": b'',
    "CLIENT_ID": b'esp_8266-' + ubinascii.hexlify(machine.unique_id())
}

# Attempting to connect to WiFi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(WIFI_CONFIG["SSID"], WIFI_CONFIG["PASS"])

connect_counter = 0
print("Waiting to Connect to Wifi")

utime.sleep(1)

while station.isconnected() == False:
    print("Trying Again")
    station.active(True)
    station.connect(WIFI_CONFIG["SSID"], WIFI_CONFIG["PASS"])
    utime.sleep(5)
    connect_counter += 1

    if connect_counter > 5:
        sys.exit()

print('WiFi Connection successful:', end=" ")
print(station.ifconfig())
