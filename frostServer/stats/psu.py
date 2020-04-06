import re
import os

def sensorReading(sensor):
    sensorStream = os.popen(f'sensors | grep {sensor}')
    if sensorStream.read():
        sensor = re.sub('^[^:]+:\s*', '', sensorStream.read())
        sensor = re.sub('[^0-9^.]*', '', sensor)
    else:
        sensor = ""
    return sensor

def power():    
    return sensorReading('power')

def voltage():
    return sensorReading('in1')

def current():
    return sensorReading('curr1')
