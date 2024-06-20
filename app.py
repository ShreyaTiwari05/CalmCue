from flask import Flask, render_template, Response
import cv2
import numpy as np
import dlib
import time
import scipy.spatial
import matplotlib.pyplot as plt
from keras.preprocessing.image import img_to_array
from keras.models import load_model
app = Flask(__name__)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:\Users\APURVA\Downloads\Stress-Detection-master\Stress-Detection-master\shape_predictor_68_face_landmarks.dat\shape_predictor_68_face_landmarks.dat")
emotion_classifier = load_model("C:\Users\APURVA\Downloads\Stress-Detection-master\Stress-Detection-master\_mini_XCEPTION.102-0.66.hdf5", compile=False)
def gen_frames():
    cap = cv2.VideoCapture(0)
    points = []

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=500, height=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = detector(gray, 0)

        for detection in detections:
            shape = predictor(gray, detection)
            shape = face_utils.shape_to_np(shape)

            (lBegin, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
            (rBegin, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]

            leyebrow = shape[lBegin:lEnd]
            reyebrow = shape[rBegin:rEnd]

            reyebrowhull = cv2.convexHull(reyebrow)
            leyebrowhull = cv2.convexHull(leyebrow)

            cv2.drawContours(frame, [reyebrowhull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [leyebrowhull], -1, (0, 255, 0), 1)

            distq = scipy.spatial.distance.euclidean(leyebrow[-1], reyebrow[0])
            points.append(int(distq))

            emotion = emotion_finder(detection, gray)
            cv2.putText(frame, emotion, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            stress_value, stress_label = normalize_values(points, distq)
            cv2.putText(frame, "stress level:{}".format(str(int(stress_value * 100))), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
