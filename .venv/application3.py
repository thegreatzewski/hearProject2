from flask import Flask, render_template, request
from pythonosc import udp_client, osc_message_builder, osc_bundle_builder
import time

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
    client = udp_client.SimpleUDPClient("192.168.1.77", 6448)   #for osc
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

    if len(volumeList) > 9:
        volumeList.pop(0)
      
    if keyID not in keyIDlist:             #this bit is checking whether the keyid is already in either position of the array
        data_list = [keyID , volume_data]    #data_list is just one client and its accompanying data
        dataIDlist.insert(0, data_list)                                                 #add to the list of all clients if not

    if len(keyIDlist) > 0:              #if there is a client, for every addition to the array(if the keyID already exists) add its volume to the second position of volume_data
        count = 0
        for i in keyIDlist:
            if keyID == i:
                dataIDlist[count][1] = volume_data     #set the specific position in the array = volume data
            count=count+1

        # and heres the osc sending business 
    funVariable = [0.0]*10   #sets up list of fixed length, justdata will stay this length           ###justdatalist!###
    addStart = len(funVariable) - len(volumeList) #this chunk adds two lists of different sizes to create a list of 10 with only volume data and zeros(if less than 10 people have connected)
    count3 = 0                                                                 
    for i in volumeList:
        funVariable[addStart+count3] = i + funVariable[addStart+count3]
        count3=count3+1
    if len(funVariable) > 9:
        funVariable.pop(9)
    print("FUN VARIABLE IS:" , funVariable)                                                                 ###funvariable###

    client = udp_client.SimpleUDPClient('192.168.1.37:5000', 6448)
    

    bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
    msg = osc_message_builder.OscMessageBuilder(address="/jake/inputs")
    for val in funVariable:
        msg.add_arg(val)
        print(val)
        time.sleep(1)
    
    bundle.add_content(msg.build())
    client.send(bundle.build())

    return {}

def extractKeyID(lst):                     #for loop function extracts each keyId 
    return [item[0] for item in lst]

def extractVolume(lst):                     #for loop function extracts each keyId 
    return [item[1] for item in lst]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')