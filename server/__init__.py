import os
from flask import Flask, render_template, Response, request, jsonify
import cv2

import laneModel
import signModel
import vehicleModel
import frame as fm
import stats
import ui_bridge as ui

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

application = Flask(__name__)

gamepadNode = fm.Node(
    subject = None,
    strategy = lambda package: package)

frameSubject = fm.Subject(0)
models = {}
models['lane'] = laneModel.generate(frameShape = frameSubject.frameShape)
models['sign'] = signModel.generate(frameShape = frameSubject.frameShape)    
models['vehicle'] = vehicleModel.generate()

models['sign']("NMS", "interpreted").addObservers(models['vehicle']("signs", "storage"))
# models['lane']("Error", "interpreted").addObservers(
#     models['vehicle']['driveController'],
#     models['vehicle']['steeringController'])

frameSubject.addObserver('sign', models['sign'].head)
frameSubject.addObserver('lane', models['lane'].head)
models['lane']("TotalError", "interpreted").addObservers(models['vehicle']("controlPackager", "control"))

imager = fm.Imager(defaultSubject = frameSubject)
imageResponder = fm.ImageResponder(imager)

frameSubject.startThreadedCapture()


@application.route('/')
def index(): return render_template('index.html')

@application.route('/gamepad', methods=['POST'])
def gamepad():
    #gamepadNode(request.json)
    models['vehicle']("controller", "control")(request.json)
    return ('', 204)

def modelToButtonCategories(model):
    categories = ui.Categories()
    
    category = ui.ButtonCategory("toggle")
    category.addButtons(model.category("annotator").keys())
    categories.addCategory("Annotation", category)
    
    category = ui.ButtonCategory("radio")
    category.addButtons(model.category("framer").keys())
    categories.addCategory("Frame", category)

    return categories


@application.route('/imageStreamChoices')
def imageStreamChoices():
    categories = ui.Categories()
    for model in models.values():
        categories += modelToButtonCategories(model)

    print(categories.asDict())        
    categories["Frame"].addButtons(["Raw"])
    categories["Frame"].addDefaults(["Raw"])

    return jsonify(categories.asDict())


@application.route('/updateImageStream', methods=['POST'])
def updateImageStream():
    def nodeFromFrameKey(frameKey):
        return frameSubject if frameKey == 'Raw' else models['lane'](frameKey, "framer")
    
    imager.subject = nodeFromFrameKey(request.json['Frame'])
    
    imager.annotatorNodes = []
    for annotator in request.json['Annotation']:
        for model in models.values():
            if annotator in model.category("annotator"):
                imager.annotatorNodes.append(model(annotator, "annotator"))
    
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
