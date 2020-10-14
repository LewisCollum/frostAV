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

frost = model.Frost(Camera(0))
frost.start()

@application.route('/')
def index(): return render_template('index.html')

@application.route('/gamepad', methods=['POST'])
def gamepad():
    frost.updateController(request.json)
    return ('', 204)

@application.route('/imageStreamChoices')
def imageStreamChoices():
    return jsonify(frost.generateButtonCategories().asDict())

@application.route('/updateImageStream', methods=['POST'])
def updateImageStream():
    frost.updateImager(frame = request.json['Frame'], annotators = request.json['Annotation'])    
    return ('', 204)

imageResponder = nodal_frost.ImageResponder(frost.imager)
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
