from flask import render_template, Response
from flaskBird import app, CameraWorker
import requests

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

def gen(cameraWorker):
    while True:
        frame = cameraWorker.analyze_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/static_preview')
def static_preview():
    req = requests.get('http://10.0.1.33:8080/?action=snapshot')
    return Response(
        req.iter_content(),
        content_type=req.headers['content-type'])

@app.route('/video_feed')
def video_feed():
    return Response(
        gen(CameraWorker()),
        mimetype='multipart/x-mixed-replace;boundary=frame')
