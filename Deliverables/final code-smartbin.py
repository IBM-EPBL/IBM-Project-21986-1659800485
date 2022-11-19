import time
import sys
import ibmiotf.application
import ibmiotf.device
import random


#Provide your IBM Watson Device Credentials
organization = "z7l8rv"
deviceType = "bin"
deviceId = "smartbin45"
authMethod = "token"
authToken = "987654321"

# Initialize GPIO
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command'])
    status=cmd.data['command']
   

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #Get Sensor Data from ultrosonic sensor
        
        t=random.randint(0,100)
        a="BIN IS GOING TO FULL" if t>=90 else "BIN IS AVAILABLE TO COLLECT WASTE"
        latitude=13.082680
        longitude=80.270721
        data = { 'level' : t ,"status" : a,'latitude' : latitude,'longitude' : longitude}
        
        #print data
        def myOnPublishCallback():
            print ("BIN LEVEL = %s"% t,"BIN STATUS : %s"% a)
            


        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback)

        if not success:
            print("Not connected to IoTF")
        time.sleep(5)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
