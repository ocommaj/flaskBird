import os
import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

CWD_PATH = os.getcwd()
MODEL_DIR = "tfmodel/"
MODEL_FILE = "birds-model.tflite"
LABEL_FILE = "birds-label.txt"
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_DIR,LABEL_FILE)
PATH_TO_MODEL = os.path.join(CWD_PATH,MODEL_DIR,MODEL_FILE)
MIN_CONF_THRESHOLD = 0.4

IMAGE_W = 656
IMAGE_H = 488

class CameraWorker(object):
    def __init__(self):
        self.video = cv2.VideoCapture("http://birdpi:8080/?action=stream")
        self.labels = load_labels()
        self.interpreter = Interpreter(PATH_TO_MODEL)
        self.interpreter.allocate_tensors()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

    def analyze_frame(self):
        ret, frame = self.video.read()

        #try:
        results = classify_image(self.interpreter, frame)
        label_id, prob = results[0]
        print("bird: " + self.labels[label_id])
        print("prob: " + str(prob))

        #finally:
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def set_input_tensor(interpreter, image):
    frame = image.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (224, 224))

    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = frame_resized

def classify_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]

def test_func():
    print(CWD_PATH)
    print(PATH_TO_LABELS)

def load_labels():
    with open(PATH_TO_LABELS, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}
