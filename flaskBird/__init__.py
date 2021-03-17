from flask import Flask
from sassutils.wsgi import SassMiddleware
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'flaskBird': ('static/sass', 'static/css', '/static/css')
})

from flaskBird.cameraWorker import CameraWorker
import flaskBird.routes
