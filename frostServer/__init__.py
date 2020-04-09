import os
from flask import Flask, render_template, Response, request, jsonify
import time 
import cv2

import laneModel
import signModel
import frame as fm
import stats
import vic

application = Flask(__name__)

frameSubject = fm.Subject(0)
models = {
    'lane': laneModel.generateForFrameSubject(frameSubject),
    'sign': signModel.generateForFrameSubject(frameSubject)}
#for name, model in models.items():
#    frameSubject.addObserver(name, model.head)
frameSubject.addObserver('sign', models['sign'].head)
imager = fm.Imager(defaultSubject = frameSubject)
imageResponder = fm.ImageResponder(imager)
#vehicle = vic.VehicleInterfaceController(crossTrackSubject = models.get('CrossTrackError'))
frameSubject.startThreadedCapture()


@application.route('/')
def index(): return render_template('index.html')

@application.route('/gamepad', methods=['POST'])
def gamepad():
    vehicle.manualUpdate(request.json)
    return ('', 204)

@application.route('/imageStreamChoices')
def imageStreamChoices():
    selections = {
        'frames': [],
        'annotators': [],
        'switchables': []
    }
    
    for model in models.values():
        for name, values in model.asDict().items():
            selections[name] += values
            
    selections['frames'] += ['Raw']
    
    return jsonify(selections)


@application.route('/updateImageStream', methods=['POST'])
def updateImageStream():
    def nodeFromFrameKey(frameKey):
        return frameSubject if frameKey == 'Raw' else models['lane'].get(frameKey)
    
    imager.subject = nodeFromFrameKey(request.json['frame'])
    
    imager.annotatorNodes = []
    for annotator in request.json['annotators']:
        for model in models.values():
            if annotator in model.annotators:
                imager.annotatorNodes.append(model.getAnnotator(annotator))
    
    models['lane'].switchables.matchNames(request.json['switchables'])
    
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
