import os
from flask import Flask, render_template, Response, request, jsonify
import time 
import cv2

import laneModel
import frame as fm
import stats
import vic

application = Flask(__name__)

frameSubject = fm.Subject(0)
model = laneModel.generateForFrameSubject(frameSubject)
frameSubject.addObserver('laneModel', model.head)
imager = fm.Imager(defaultSubject = frameSubject)
imageResponder = fm.ImageResponder(imager)

vehicle = vic.VehicleInterfaceController(crossTrackSubject = model.get('CrossTrackError'))

frameSubject.startThreadedCapture()

@application.route('/')
def index(): return render_template('index.html')

@application.route('/gamepad', methods=['POST'])
def gamepad():
    vehicle.manualUpdate(request.json)
    return ('', 204)

@application.route('/imageStreamChoices')
def imageStreamChoices():
    selections = model.asDict()
    selections['frames'] += ['Raw']
    return jsonify(selections)

@application.route('/updateImageStream', methods=['POST'])
def updateImageStream():
    def nodeFromFrameKey(frameKey):
        return frameSubject if frameKey == 'Raw' else model.get(frameKey)
    
    imager.subject = nodeFromFrameKey(request.json['frame'])
    imager.annotationNodes = [model.get(annotation) for annotation in request.json['annotations']]
    model.switchables.matchNames(request.json['switchables'])
    return ('', 204)

@application.route('/imageStream')
def imageStream():   
    return Response(imageResponder, mimetype='multipart/x-mixed-replace; boundary=frame')

@application.route('/cpuCelsius')
def cpuCelsius(): return Response(stats.pi.cpuCelsius(), 'text/plain')

@application.route('/gpuCelsius')
def gpuCelsius(): return Response(stats.pi.gpuCelsius(), 'text/plain')

@application.route('/cpuLoad')
def cpuLoad(): return Response(stats.pi.cpuLoad(), 'text/plain')

@application.route('/memoryUsed')
def memoryUsed(): return Response(stats.pi.memoryUsed(), 'text/plain')

@application.route('/memoryFree')
def memoryFree(): return Response(stats.pi.memoryFree(), 'text/plain')

@application.route('/power')
def power(): return Response(stats.psu.power(), 'text/plain')

@application.route('/voltage')
def voltage(): return Response(stats.psu.voltage(), 'text/plain')

@application.route('/current')
def current(): return Response(stats.psu.current(), 'text/plain')


if __name__ == '__main__':
    os.environ["FLASK_ENV"] = "development"
    application.run(debug=True, use_reloader=False, host='0.0.0.0')
