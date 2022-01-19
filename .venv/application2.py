
# this is a remastered version of application.py
# sat jan 15 2022
# jake kaliszewski, felix loftus, conrad menchine, and many many stackexchangers
###################################################


from flask import Flask, render_template, request
from pythonosc import udp_client, osc_message_builder
import numpy
 


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

    #this is a new method for sending osc messages
   
    justDataList = [0.0]*10   #sets up list of fixed length, justdata will stay this length           ###justdatalist!###
  
    funVariable = justDataList  
    print("JUST DATALIST IS:" , justDataList) 
    print("FUN VARIABLE IS:" , funVariable)                                                                 ###funvariable###
    # addStart = len(justDataList) - len(volumeList) #this chunk adds two lists of different sizes to create a list of 10 with only volume data and zeros(if less than 10 people have connected)
    # count3 = 0                                                                  
    # for i in volumeList:
    #     funVariable[addStart+count3] = i + justDataList[addStart+count3]
    #     count3=count3+1
    # if len(funVariable) > 9:
    #     funVariable.pop(9)
    # print(funVariable)

    # msg = osc_message_builder.OscMessageBuilder(address = '/data_inputs')
    # count2 = 0
    # for keyID in dataIDlist:
    #     msg.add_arg(justDataList[count2], arg_type='f')   #add position [count2] of justdatalist to the msg 
    #     count2=count2+1
    #     print("JUST DATA LIST IS:")
    #     print(justDataList)
    #     print(funVariable)

    # msg = msg.build()
    # client.send(msg)


    # here is yet another way of sending osc

    # send_address = '192.168.1.77', 6448
    # c = OSC.OSCClient()
    # c.connect( send_address )
    # count4 = 0
    # rNum = OSC.OSCMessage()
    # rNum.setAddress("/jake/inputs")
    # for i in funVariable:
    #     n = funVariable[count4]
    #     rNum.append(n)
    #     print("sent some values: ", rNum)
    #     c.send(rNum)
    #     count4=count4+1
    # print("sent rNum all the things: ", rNum)
    
    return {}

def extractKeyID(lst):                     #for loop function extracts each keyId 
    return [item[0] for item in lst]

def extractVolume(lst):                     #for loop function extracts each keyId 
    return [item[1] for item in lst]


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')