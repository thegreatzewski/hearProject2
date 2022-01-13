from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread
from pythonosc import udp_client
#import RPi.GPIO as GPIO
dataIDlist = []        #this creates an array to store both client ids in and their volume data
keyIDlist = [] 

app = Flask(__name__,static_url_path="/")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/publish", methods=["POST", "GET"])
def post_data():
    print("volume:", request.args.get("volume"))
    print("keyID:", request.args.get("keyID"))
    client = udp_client.SimpleUDPClient("10.19.27.30", 6448)   #for osc
    volume_data = request.args.get("volume")
    keyIDlist = extractKeyID(dataIDlist)
    print(keyIDlist)
    if request.args.get("keyID") not in keyIDlist:             #this bit is checking whether the keyid is already in either position of the array
        data_list = [request.args.get("keyID") , volume_data]
        dataIDlist.append(data_list)                                                 #add to the list if not
    print("the keyID list is")
    print(dataIDlist)
    

    # keyID_data = request.args.get("keyID")
    print(volume_data)
    if volume_data != None:
        client.send_message("/volumeosc", volume_data)
        print("data sent")

    if len(keyIDlist) > 0:              #if there is a client, for every addition to the array(if the keyID already exists) add its volume to the second position of volume_data
        count = 0
        for i in keyIDlist:
            if request.args.get("keyID") == i:
                dataIDlist[count][1] = volume_data     #set the specific position in the array = volume data
            count=count+1

    return {}

def extractKeyID(lst):
    return [item[0] for item in lst]



# @socketio.on('volume')
# # def test_message(data):
# def test_message(message):
#     emit('my response', {'data': 'got it!'})
#     print('received message: ' + 'data')         



if __name__ == "__main__":

    #socketio.run(app)

    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
    
