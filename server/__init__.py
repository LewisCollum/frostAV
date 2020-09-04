from flask import Flask, render_template, Response, request, jsonify

from autonomy.sensing import Camera
import model
import nodal_frost
import stats
import ui_bridge as ui

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

application = Flask(__name__)

frostModels = model.generateForCamera(Camera(0))
imager = nodal_frost.Imager(defaultSubject = frostModels['sensing']("Camera", "framer"))
imageResponder = nodal_frost.ImageResponder(imager)
frostModels['sensing']("Camera", "framer").start()

@application.route('/')
def index(): return render_template('index.html')

@application.route('/gamepad', methods=['POST'])
def gamepad():
    frostModels['vehicle']("controller", "control")(request.json)
    return ('', 204)

@application.route('/imageStreamChoices')
def imageStreamChoices():
    categories = ui.Categories()
    for frostModel in frostModels.values():
        categories += model.toButtonCategories(frostModel)

    print(categories.asDict())        
    categories["Frame"].addDefaults(["Camera"])

    return jsonify(categories.asDict())


@application.route('/updateImageStream', methods=['POST'])
def updateImageStream():
    frameKey = request.json['Frame']
    imager.annotatorNodes = []
    annotators = request.json['Annotation']
    
    for frostModel in frostModels.values():
        if frameKey in frostModel.category("framer"):
            imager.subject = frostModel(frameKey, "framer")
            break

    for annotator in annotators:
        for frostModel in frostModels.values():            
            if annotator in frostModel.category("annotator"):
                imager.annotatorNodes.append(frostModel(annotator, "annotator"))
    
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
    import os    
    os.environ["FLASK_ENV"] = "development"
    application.run(debug=True, use_reloader=False, host='0.0.0.0')
