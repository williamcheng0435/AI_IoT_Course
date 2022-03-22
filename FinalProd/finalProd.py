#Based on https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi

#Flask import
import flask
from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import Response

#Tflite
import argparse
import sys
import time

import cv2
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import detect
import utils


#page name
app = Flask(__name__)


#main page
@app.route("/")
def index():
    #return "<p>This is the index page <br> Hello World!</p>"
    return render_template('index.html')
#end of main page


#streaming part
#camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''
def gen_frames(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool) -> None:  # generate frame by frame from camera
    
    
    #start the immersing
    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()

    # Start capturing video input from the camera
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Visualization parameters
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=num_threads,
        score_threshold=0.3,
        max_results=3,
        enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            sys.exit(
            'ERROR: Unable to read from webcam. Please verify your webcam settings.'
        )

        counter += 1
        frame = cv2.flip(frame, 1)

        # Run object detection estimation using the model.
        detections = detector.detect(frame)

        # Draw keypoints and edges on input image
        frame = utils.visualize(frame, detections)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        text_location = (left_margin, row_size)
        cv2.putText(frame, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    font_size, text_color, font_thickness)

        
    
    #end

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        
        # Stop the program if the ESC key is pressed.
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames('detect_test.tflite',0,640,480,4,False), mimetype='multipart/x-mixed-replace; boundary=frame')
#end of streaming


if __name__ == "__main__":
    #debug true for easy editing
    #hosting is making it externally visible
    #app.run(host= '192.168.0.101', port=5000, debug=True)
    #debug = true has bug
    app.run(host= '192.168.0.104', port=5000, debug=False)