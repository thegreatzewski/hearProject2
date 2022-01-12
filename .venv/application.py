from flask import Flask, render_template, request
from flask_socketio import SocketIO
from threading import Thread
from pythonosc import udp_client
#import RPi.GPIO as GPIO



app = Flask(__name__,static_url_path="/")
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/publish", methods=["POST", "GET"])
def post_data():
    print("volume:", request.args.get("volume"))
    client = udp_client.SimpleUDPClient("10.19.27.30", 6448)
    volume_data = request.args.get("volume")
    print(volume_data)
    if volume_data != None:
        client.send_message("/volumeosc", volume_data)
        print("data sent")
    return {}

# @socketio.on('volume')
# def handle_message(data):
#     print('received message: ' + data)         



if __name__ == "__main__":

    # socketio.run(app)

    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
    
