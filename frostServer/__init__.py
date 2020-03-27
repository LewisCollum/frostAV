#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import time
import re
import time 

import camera_opencv as camera
import source as s

def onFrame(frame):
    s.frame_distributor.sendFrame(frame)
    return s.inout.outputNode.output
camera.onFrame = onFrame

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')


def asImageResponse(frame):
    return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

@application.route('/video_feed')
def video_feed():
    def generate():
        camera.startReading()
        while True:
            frame = camera.getFrame() 
            if frame:
                yield asImageResponse(frame)
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@application.route('/cpuCelsius')
def cpuCelsius():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as cpuCelsiusFile:
        cpuCelsius = str(round(int(cpuCelsiusFile.readline())/1000))
        return Response(cpuCelsius, 'text/plain')

@application.route('/gpuCelsius')
def gpuCelsius():
    stream = os.popen('/opt/vc/bin/vcgencmd measure_temp');
    gpuCelsius = str(int(re.sub('[^0-9]', '', stream.read())) / 10)
    return Response(gpuCelsius, 'text/plain')

@application.route('/cpuLoad')
def cpuLoad():
    with open('/proc/loadavg', 'r') as cpuLoadFile:
        load = cpuLoadFile.readline()[:4]
        return Response(load, 'text/plain')

@application.route('/memoryUsed')
def memoryUsed():
    freeMemoryStream = os.popen('cat /proc/meminfo | grep MemFree')
    totalMemoryStream = os.popen('cat /proc/meminfo | grep MemTotal')
    freeMemory = int(re.sub('[^0-9]', '', freeMemoryStream.read()))
    totalMemory = int(re.sub('[^0-9]', '', totalMemoryStream.read()))
    usedMemory = totalMemory - freeMemory
    usedMemoryReadable = str(round(usedMemory/1024))
    return Response(usedMemoryReadable, 'text/plain')

@application.route('/memoryFree')
def memoryFree():
    freeMemoryStream = os.popen('cat /proc/meminfo | grep MemFree')
    freeMemory = int(re.sub('[^0-9]', '', freeMemoryStream.read()))
    freeMemoryReadable = str(round(freeMemory/1024))
    return Response(freeMemoryReadable, 'text/plain')


def sensorReading(sensor):
    sensorStream = os.popen(f'sensors | grep {sensor}')
    if sensorStream.read():
        sensor = re.sub('^[^:]+:\s*', '', sensorStream.read())
        sensor = re.sub('[^0-9^.]*', '', sensor)
    else:
        sensor = ""
    return sensor

@application.route('/power')
def power():    
    return Response(sensorReading('power'), 'text/plain')

@application.route('/voltage')
def voltage():
    return Response(sensorReading('in1'), 'text/plain')

@application.route('/current')
def current():
    return Response(sensorReading('curr1'), 'text/plain')


import smbus2
vehicleControllerAddress = 0x32
@application.route('/gamepad', methods=['POST'])
def gamepad():
    steering, forward, reverse = request.values.get('input', '').split(',')
    mappedSteering = int(10*(float(steering) - (-0.8))/1.6)
    mappedForward = int(20*(float(forward) - (-0.8))/1.7)
    mappedReverse = int(20*(float(reverse) - (-0.8))/1.7)    
    output = f'{str(mappedSteering)},{str(mappedForward)},{str(mappedReverse)}'
    
    with smbus2.SMBus(1) as bus:
        message = smbus2.i2c_msg.write(vehicleControllerAddress, output)
        bus.i2c_rdwr(message)
    return output


if __name__ == '__main__':
    application.run(host='0.0.0.0')
