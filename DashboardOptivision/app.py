from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from Detector import Detector
import os
import subprocess
from werkzeug.utils import secure_filename
import csv
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit

modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/centernet_resnet101_v1_fpn_512x512_coco17_tpu-8.tar.gz"
classFile = "coco.names"
detector = Detector(modelURL, classFile)

# ---------- Base Routes ----------

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/process-image', methods=['GET'])
def processimage():
    return render_template('images.html')

@app.route('/process-video', methods=['GET'])
def processvideo():
    return render_template('videos.html')

@app.route('/process-rtsp', methods=['GET'])
def processrtsp():
    return render_template('stream.html')

@app.route('/chatbot', methods=['GET'])
def chatbot():
    return render_template('chatbot.html')

# ---------- Upload Handlers ----------

@app.route('/process-image', methods=['POST'])
def process_image():
    image = request.files['image']
    if image:
        filename = secure_filename(image.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)

        pathresult = detector.predictImage(path)
        return send_file(pathresult, mimetype='image/jpeg')  # Return processed image
    return redirect(url_for('index'))

@app.route('/process-video', methods=['POST'])
def process_video():
    video = request.files['video']
    if video:
        filename = secure_filename(video.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(path)

        detector.predictVideoSource(path)
        return f"Video processed: {filename}"
    return redirect(url_for('index'))

@app.route('/process-rtsp', methods=['POST'])
def process_rtsp():
    channel = request.form['channel']
    if channel:
        subprocess.Popen(["python", "RTSP_cam.py", "--channel", channel])
        return f"RTSP Stream for Channel {channel} is running."
    return redirect(url_for('index'))

# ---------- Analytics Routes ----------

@app.route('/metrics', methods=['GET'])
def metrics_page():
    return render_template('analytics.html')  # You must create this HTML file

@app.route('/api/metrics')
def get_metrics():
    start = request.args.get('start_date')
    end = request.args.get('end_date')
    
    # Define the date format explicitly to avoid the warning
    date_format = "%d-%m-%Y %I:%M:%S %p"  # Adjust format to match the 'Date' and 'Time (IST)' columns

    # Read CSV with custom date parsing
    df = pd.read_csv('detection_log2.csv', parse_dates=[['Date', 'Time (IST)']], 
                     date_parser=lambda x: pd.to_datetime(x, format=date_format))
    df['Date'] = pd.to_datetime(df['Date_Time (IST)']).dt.date
    
    # Filter the dataframe based on the given date range
    filtered = df[(df['Date'] >= pd.to_datetime(start).date()) & (df['Date'] <= pd.to_datetime(end).date())]
    
    # Group the data by date and count occurrences
    trend = filtered.groupby('Date').size().reset_index(name='count')

    return jsonify({
        'dates': trend['Date'].astype(str).tolist(),
        'counts': trend['count'].tolist()
    })



if __name__ == '__main__':
    app.run(debug=True, port=5100)
