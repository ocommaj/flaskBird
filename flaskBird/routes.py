from flask import render_template, Response
from flaskBird import app, CameraWorker

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

def gen(cameraWorker):
    while True:
        #frame = cameraWorker.get_frame()
        frame = cameraWorker.analyze_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(
        gen(CameraWorker()),
        mimetype='multipart/x-mixed-replace;boundary=frame')
