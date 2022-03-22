import flask
from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
from flask import Response

import cv2


app = Flask(__name__)

#main page
@app.route("/")
def index():
    #return "<p>This is the index page <br> Hello World!</p>"
    return render_template('index.html')

#pass parameter by url
@app.route('/user/<username>')
def username(username):
    return 'Username is: ' + username

@app.route('/age/<int:age>')
def userage(age):
    return 'i am ' + str(age) + ' years old'
#end of examples

#redirect examples
@app.route('/a')
def url_for_a():
    return 'here is a'

@app.route('/b')
def b():
    #  redirect user to '/a' route
    return redirect(url_for('url_for_a'))
#end of examples

#streaming part
camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''
def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        _, frame = camera.read()  # read the camera frame
        """
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        """
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
#end of streaming


if __name__ == "__main__":
    #debug true for easy editing
    #hosting is making it externally visible
    #app.run(host= '192.168.0.101', port=5000, debug=True)
    #debug = true has bug
    app.run(host= '192.168.0.104', port=5000, debug=False)