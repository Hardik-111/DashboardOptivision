from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
import os
from Detector import Detector
import cv2
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
RESULT_FOLDER = os.path.join('static', 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/centernet_resnet101_v1_fpn_512x512_coco17_tpu-8.tar.gz"
classFile = "coco.names"

  #  root = tk.Tk()
detector = Detector(modelURL, classFile)
#detector = Detector()  # Assumes it handles all modes internally

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            result_path = os.path.join(RESULT_FOLDER, f"result_{filename}")
            file.save(upload_path)
            detector.detect_image(upload_path, result_path)
            return render_template('image.html', uploaded=True, result_image=result_path)
    return render_template('image.html', uploaded=False)

@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == 'POST':
        file = request.files['video']
        if file:
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            result_path = os.path.join(RESULT_FOLDER, f"result_{filename}")
            file.save(upload_path)
            detector.detect_video(upload_path, result_path)
            return render_template('video.html', uploaded=True, result_video=result_path)
    return render_template('video.html', uploaded=False)

@app.route('/stream', methods=['GET', 'POST'])
def stream():
    if request.method == 'POST':
        rtsp_url = request.form['rtsp_url']
        return redirect(url_for('stream_feed', rtsp_url=rtsp_url))
    return render_template('stream.html')

@app.route('/stream_feed')
def stream_feed():
    rtsp_url = request.args.get('rtsp_url')

    def generate():
        for frame in detector.detect_stream(rtsp_url):
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)
