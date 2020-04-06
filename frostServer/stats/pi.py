import re
import os

def cpuCelsius():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as cpuCelsiusFile:
        cpuCelsius = str(round(int(cpuCelsiusFile.readline())/1000))
        return cpuCelsius

def gpuCelsius():
    stream = os.popen('/opt/vc/bin/vcgencmd measure_temp');
    gpuCelsius = str(int(re.sub('[^0-9]', '', stream.read())) / 10)
    return gpuCelsius


def cpuLoad():
    with open('/proc/loadavg', 'r') as cpuLoadFile:
        load = cpuLoadFile.readline()[:4]
        return load


def memoryUsed():
    freeMemoryStream = os.popen('cat /proc/meminfo | grep MemFree')
    totalMemoryStream = os.popen('cat /proc/meminfo | grep MemTotal')
    freeMemory = int(re.sub('[^0-9]', '', freeMemoryStream.read()))
    totalMemory = int(re.sub('[^0-9]', '', totalMemoryStream.read()))
    usedMemory = totalMemory - freeMemory
    usedMemoryReadable = str(round(usedMemory/1024))
    return usedMemoryReadable

def memoryFree():
    freeMemoryStream = os.popen('cat /proc/meminfo | grep MemFree')
    freeMemory = int(re.sub('[^0-9]', '', freeMemoryStream.read()))
    freeMemoryReadable = str(round(freeMemory/1024))
    return freeMemoryReadable
