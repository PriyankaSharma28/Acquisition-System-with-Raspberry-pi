
#MLX90614-Temp Signal Acquisition

from smbus2 import SMBus
from mlx90614 import MLX90614
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
print ("Ambient Temp=", sensor.get_amb_temp())
print ("Object Temp=", sensor.get_obj_temp())
bus.close()
       

#MAX30102-PPG Signal Acquisition

from heartrate_monitor import HeartRateMonitor
import time
import argparse

parser = argparse.ArgumentParser(description="Read and print data from MAX30102")
parser.add_argument("-r", "--raw", action="store_true",
                    help="print raw data instead of calculation result")
parser.add_argument("-t", "--time", type=int, default=30,
                    help="duration in seconds to read from sensor, default 30")
args = parser.parse_args()

print('sensor starting...')
hrm = HeartRateMonitor(print_raw=args.raw, print_result=(not args.raw))
hrm.start_sensor()
try:
    time.sleep(args.time)
except KeyboardInterrupt:
    print('keyboard interrupt detected, exiting...')

hrm.stop_sensor()
print('sensor stoped!')


#AD8232-ECG Signal Acquisition

#!/usr/bin/python
#--------------------------------------   
# This script reads data from a 
# MCP3008 ADC device using the SPI bus.
#
# Author : Valliappan
# Date   : 14/04/2016
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import spidev
import time
import os
import array
import pylab as pl
NUM_channel = 8
ECG_print=[0 for i in range(NUM_channel) ]
ECG_volts=[]

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz = 1000000

# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places. 
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)  
  return volts
  
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):

  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  388       75    1.25
  #  465      100    1.50
  #  543      125    1.75
  #  620      150    2.00
  #  698      175    2.25
  #  775      200    2.50
  #  853      225    2.75
  #  930      250    3.00
  # 1008      275    3.25
  # 1023      280    3.30

  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp
  
# Define sensor channels

ECG_channel = 0


# Define delay between readings
delay = 0.1
i = 0
while i<600:
    time.sleep(0.1)
    ECG_level= ReadChannel(ECG_channel)
    ECG_volts.append(ConvertVolts(ECG_level,2))
  # Read the light sensor data
  #ECG_level = ReadChannel(ECG_channel)
 # print(ECG_level)
 
 
  # Read the temperature sensor data
  #temp_level = ReadChannel(temp_channel)
  #temp_volts = ConvertVolts(temp_level,2)
  #temp       = ConvertTemp(temp_level,2)

  # Print out results
    print ("--------------------------------------------")
    print("ECG_volts : {} ({}V)".format(i,ECG_volts[i]))  
  #print("Temp  : {} ({}V) {} deg C".format(temp_level,temp_volts,temp))    

  # Wait before repeating loop
    i = i+1
pl.plot(ECG_volts,label="ECG")
pl.legend()
pl.show()
