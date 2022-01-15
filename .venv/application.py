from flask import Flask, render_template, request
#from flask_socketio import SocketIO, emit
from threading import Thread
from pythonosc import udp_client
#import RPi.GPIO as GPIO
import numpy 

dataIDlist = []        #this creates an array to store both client ids in and their volume data
keyIDlist = []
oscInputList = []
preOscInputList = []     #   /\  it turns out wekinator expects inputs in a different form, ex for 4 inputs: [/oscInputList, 0.3323 , 0.0441 , 0.0619 , 0.111]    i think
prepreOscInputList = []

app = Flask(__name__,static_url_path="/")
app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/publish", methods=["POST", "GET"])
def post_data():
    print("VOLUME:", request.args.get("volume"))
    print("KEYID:", request.args.get("keyID"))
    print("THE KEYID LIST IS:")
    #print(keyIDlist)
    print("THE DATAID LIST IS:")
    print(dataIDlist)

    client = udp_client.SimpleUDPClient("10.19.27.30", 6448)   #for osc
    volume_data = request.args.get("volume")
    keyIDlist = extractKeyID(dataIDlist)

    if request.args.get("keyID") not in keyIDlist:             #this bit is checking whether the keyid is already in either position of the array
        data_list = [request.args.get("keyID") , volume_data]
        dataIDlist.append(data_list)                                                 #add to the list if not

    print(numpy.float32(volume_data))

    # keyID_data = request.args.get("keyID")
    volume_data32 = numpy.float32(volume_data)
    print(volume_data)
    if volume_data != None:
        client.send_message("/volumeosc_1/", volume_data32 )
        print("test OSCDATA SENT")

    if len(keyIDlist) > 0:              #if there is a client, for every addition to the array(if the keyID already exists) add its volume to the second position of volume_data
        count = 0
        for i in keyIDlist:
            if request.args.get("keyID") == i:
                dataIDlist[count][1] = volume_data     #set the specific position in the array = volume data
            count=count+1

    count = 0                               #send osc
    for volume_data in dataIDlist:
        pretag = "/keyID"
        tag = pretag + str([count][0])
        client.send_message(tag, volume_data)
        print(tag + "  IS THE TAG ")    
        count=count+1
        
    # prepreOscInputList = [0.0]*10
    # count = 0
    # for volume_data in dataIDlist:
    #     prepreOscInputList[count] = volume_data
    #     count=count+1
    #     # for item in prepreOscInputList:
    #     #     preOscInputList.append(float(item))

    # oscInputList = ["/oscInputList" , preOscInputList[0] , preOscInputList[1] , preOscInputList[2], preOscInputList[3] , preOscInputList[4] , preOscInputList[5] , preOscInputList[6] , preOscInputList[7] , preOscInputList[8] , preOscInputList[9]]
    # print(oscInputList)

    #.pop(thatelement) if volume data is unchanging 
   
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
    
