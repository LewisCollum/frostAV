import os
from flask import Flask, render_template, Response, request, jsonify
import time 
import cv2

#import vehicleModel
import laneModel
import signModel
import frame as fm
import stats
import ui_bridge as ui
#import vic

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

application = Flask(__name__)

gamepadNode = fm.Node(
    name = 'gamepad',
    subjects = [],
    strategy = lambda package: package)

frameSubject = fm.Subject(0)
models = {}
models['lane'] = laneModel.generate(subject = frameSubject)
models['sign'] = signModel.generate(subject = frameSubject)    
#models['vehicle'] = vehicleModel.generate()

#models['sign']['NMS'].addObservers([models['vehicle']['signs']])
# models['lane']['Error'].addObservers([
#     models['vehicle']['driveController'],
#     models['vehicle']['steeringController']])

frameSubject.addObserver('sign', models['sign'].head)
frameSubject.addObserver('lane', models['lane'].head)
#models['lane']['TotalError'].addObservers([models['vehicle']['controlPackager']])

imager = fm.Imager(defaultSubject = frameSubject)
imageResponder = fm.ImageResponder(imager)

frameSubject.startThreadedCapture()


@application.route('/')
def index(): return render_template('index.html')

@application.route('/gamepad', methods=['POST'])
def gamepad():
    #gamepadNode(request.json)
    models['vehicle']['controller'](request.json)
    return ('', 204)

@application.route('/imageStreamChoices')
def imageStreamChoices():
    categories = ui.Categories()
    for model in models.values():
        categories += ui.modelToButtonCategories(model)

    categories['Frame'].addButtons(['Raw'])
    categories['Frame'].addDefaults(['Raw'])

    return jsonify(categories.asDict())


@application.route('/updateImageStream', methods=['POST'])
def updateImageStream():
    def nodeFromFrameKey(frameKey):
        return frameSubject if frameKey == 'Raw' else models['lane'].get(frameKey)
    
    imager.subject = nodeFromFrameKey(request.json['Frame'])
    
    imager.annotatorNodes = []
    for annotator in request.json['Annotation']:
        for model in models.values():
            if annotator in model.annotators:
                imager.annotatorNodes.append(model.getAnnotator(annotator))
    
    models['lane'].switchables.matchNames(request.json['Switchable'])
    
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
