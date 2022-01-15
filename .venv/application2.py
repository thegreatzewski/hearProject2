
# this is a remastered version of application.py
# sat jan 15 2022
# jake kaliszewski, felix loftus, conrad menchine
###################################################


from flask import Flask, render_template, request
from pythonosc import udp_client, osc_message_builder
import numpy
from itertools import zip_longest

dataIDlist = []        #this creates an array to store both client ids in and their volume data
keyIDlist = []
volumeList = []
#dataidlist has both values like this [id,volume]

app = Flask(__name__,static_url_path="/")

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/publish", methods=["POST", "GET"])
def post_data():

    keyIDlist = extractKeyID(dataIDlist)
    volumeList = extractVolume(dataIDlist)
    client = udp_client.SimpleUDPClient("10.19.27.30", 6448)   #for osc
    volume_data = request.args.get("volume")
    volume_data = ((float(volume_data))*1000) 
    keyID = request.args.get("keyID")
    print(volume_data)

    print("VOLUME:", request.args.get("volume"))
    print("KEYID:", request.args.get("keyID"))
    print("KEYID LIST IS:" , keyIDlist)
    print("DATAID LIST IS:" , dataIDlist) 
    print("VOLUME LIST IS:" , volumeList) 
    intVolumeList = [int(z) for z in volumeList] 
      

    if keyID not in keyIDlist:             #this bit is checking whether the keyid is already in either position of the array
        data_list = [keyID , volume_data]    #data_list is just one client and its accompanying data
        dataIDlist.insert(0, data_list)                                                 #add to the list of all clients if not

    if len(keyIDlist) > 0:              #if there is a client, for every addition to the array(if the keyID already exists) add its volume to the second position of volume_data
        count = 0
        for i in keyIDlist:
            if keyID == i:
                dataIDlist[count][1] = volume_data     #set the specific position in the array = volume data
            count=count+1

    #this is a new method for sending osc messages
    # yetAnotherList = []
    justDataList = [0]*10   #sets up list of fixed length, justdata will stay this length
    # for x in range(0,len(justDataList)):
    #     yetAnotherList.append(volumeList[x] + justDataList[x])
    # print("this is yet another list:")
    # print(yetAnotherList)

    

    # if keyID not in keyIDlist:
    #     justDataList[keyIDlist.index(keyID)] = request.args.get("volume")  #an attempt at making a list of just volumes 
 
    msg = osc_message_builder.OscMessageBuilder(address = '/py/data_inputs')
    count2 = 0
    for keyID in dataIDlist:
        msg.add_arg(justDataList[count2], arg_type='f')   #add position [count2] of justdatalist to the msg 
        if len(justDataList) > 10:
            justDataList.pop(0)
        count2=count2+1
        print("JUST DATA LIST IS:")
        print(justDataList)

    msg = msg.build()
    client.send(msg)
 
    return {}

def extractKeyID(lst):                     #for loop function extracts each keyId 
    return [item[0] for item in lst]

def extractVolume(lst):                     #for loop function extracts each keyId 
    return [item[1] for item in lst]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')