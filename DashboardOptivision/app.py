import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from datetime import datetime
from Detector import Detector
import subprocess

app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_IMAGE_FOLDER'] = 'static/result/images'
app.config['RESULT_VIDEO_FOLDER'] = 'static/result/videos'
app.config['RESULT_STREAM_FOLDER'] = 'static/result/streams'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

modelURL = "http://download.tensorflow.org/models/object_detection/tf2/20200711/centernet_resnet101_v1_fpn_512x512_coco17_tpu-8.tar.gz"
classFile = "coco.names"
detector = Detector(modelURL, classFile)

# ---------- Routes ----------

@app.route('/')
def index():
    return render_template('index.html')

# ---------- Image Routes ----------
@app.route('/process-image', methods=['GET'])
def process_image_page():
    images_path = app.config['RESULT_IMAGE_FOLDER']
    try:
        all_images = sorted(
            os.listdir(images_path),
            key=lambda x: os.path.getmtime(os.path.join(images_path, x)),
            reverse=True
        )
    except FileNotFoundError:
        all_images = []

    recent_images = all_images[:6]
    return render_template('images.html', uploaded=False, recent_images=recent_images)

@app.route('/process-image', methods=['POST'])
def process_image():
    image = request.files['image']
    if image:
        filename = secure_filename(image.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(upload_path)

        result_path = detector.predictImage(upload_path)
        result_image = os.path.basename(result_path)

        recent_images = sorted(
            os.listdir(app.config['RESULT_IMAGE_FOLDER']),
            key=lambda x: os.path.getmtime(os.path.join(app.config['RESULT_IMAGE_FOLDER'], x)),
            reverse=True
        )[:6]

        return render_template(
            'images.html',
            uploaded=True,
            result_image=result_image,
            recent_images=recent_images
        )
    return redirect(url_for('index'))

# ---------- Video Routes ----------
@app.route('/process-video', methods=['GET'])
def process_video_page():
    try:
        all_videos = sorted(
            os.listdir(app.config['RESULT_VIDEO_FOLDER']),
            key=lambda x: os.path.getmtime(os.path.join(app.config['RESULT_VIDEO_FOLDER'], x)),
            reverse=True
        )
    except FileNotFoundError:
        all_videos = []

    recent_videos = all_videos[:6]
    return render_template('videos.html', uploaded=False, recent_videos=recent_videos)

@app.route('/process-video', methods=['POST'])
def process_video():
    video = request.files['video']
    if video:
        filename = secure_filename(video.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video.save(upload_path)

        # Assuming predictVideoSource method will now return the processed video path
        processed_video_path = detector.predictVideoSource(upload_path)
        
        if processed_video_path:  # Make sure the video is processed and path exists
            result_video_filename = os.path.basename(processed_video_path)
            result_video_path = os.path.join(app.config['RESULT_VIDEO_FOLDER'], result_video_filename)
            
            try:
                # Move the processed video to the correct folder
                os.rename(processed_video_path, result_video_path)
                print(f"Moved processed video to {result_video_path}")
            except FileNotFoundError as e:
                print(f"Error moving video: {e}")
                return f"Error: {e}", 500

            # List recently processed videos
            recent_videos = sorted(
                os.listdir(app.config['RESULT_VIDEO_FOLDER']),
                key=lambda x: os.path.getmtime(os.path.join(app.config['RESULT_VIDEO_FOLDER'], x)),
                reverse=True
            )[:6]

            return render_template(
                'videos.html',
                uploaded=True,
                result_video=result_video_filename,
                recent_videos=recent_videos
            )
        else:
            return "Error: Processed video not found.", 500

    return redirect(url_for('process_video_page'))

# ---------- RTSP Stream Routes ----------
@app.route('/process-rtsp', methods=['GET'])
def process_rtsp_page():
    try:
        all_streams = sorted(
            os.listdir(app.config['RESULT_STREAM_FOLDER']),
            key=lambda x: os.path.getmtime(os.path.join(app.config['RESULT_STREAM_FOLDER'], x)),
            reverse=True
        )
    except FileNotFoundError:
        all_streams = []

    recent_streams = all_streams[:6]
    return render_template('stream.html', uploaded=False, recent_streams=recent_streams)

@app.route('/process-rtsp', methods=['POST'])
def process_rtsp():
    channel = request.form['channel']
    if channel:
        subprocess.Popen(["python", "RTSP_cam.py", "--channel", channel])

        recent_streams = sorted(
            os.listdir(app.config['RESULT_STREAM_FOLDER']),
            key=lambda x: os.path.getmtime(os.path.join(app.config['RESULT_STREAM_FOLDER'], x)),
            reverse=True
        )[:6]

        return render_template(
            'stream.html',
            uploaded=True,
            channel=channel,
            recent_streams=recent_streams
        )
    return redirect(url_for('process_rtsp_page'))

# ---------- Analytics ----------
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/metrics')
def metrics_page():
    return render_template('analytics.html')

@app.route('/api/metrics')
def get_metrics():
    start = request.args.get('start_date')
    end = request.args.get('end_date')

    date_format = "%d-%m-%Y %I:%M:%S %p"
    df = pd.read_csv('detection_log2.csv', parse_dates=[['Date', 'Time (IST)']],
                     date_parser=lambda x: pd.to_datetime(x, format=date_format))
    df['Date'] = pd.to_datetime(df['Date_Time (IST)']).dt.date

    filtered = df[(
        df['Date'] >= pd.to_datetime(start).date()) & 
        (df['Date'] <= pd.to_datetime(end).date())
    ]
    trend = filtered.groupby('Date').size().reset_index(name='count')

    return jsonify({
        'dates': trend['Date'].astype(str).tolist(),
        'counts': trend['count'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5400)
