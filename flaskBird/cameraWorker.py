import cv2

class CameraWorker(object):
    def __init__(self):
        self.video = cv2.VideoCapture("http://birdpi:8080/?action=stream")

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
