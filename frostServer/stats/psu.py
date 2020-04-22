import re
import os

def sensorReading(sensor):
    sensorStream = os.popen(f'sensors | grep {sensor}')
    sensor = sensorStream.read()
    sensor = re.sub('^[^:]+:\s*', '', sensor)
    sensor = re.sub('[^0-9^.]*', '', sensor)
    return sensor

def power():    
    return sensorReading('power1')

def voltage():
    return sensorReading('in1')

def current():
    return sensorReading('curr1')
