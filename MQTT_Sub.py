
# payload to send in the topic : application/5/device/010203040506070b/rx
""" {
   "applicationID":"5",
   "applicationName":"RB-home",
   "deviceName":"RB-feather-M0",
   "devEUI":"010203040506070b",
   "rxInfo":[
      {
         "gatewayID":"3150000000000002",
         "name":"toulouse_remi",
         "rssi":-96,
         "loRaSNR":6.2,
         "location":{
            "latitude":43.60625069174644,
            "longitude":1.4709877967834475,
            "altitude":204
         }
      }
   ],
   "txInfo":{
      "frequency":868300000,
      "dr":5
   },
   "adr":true,
   "fCnt":58,
   "fPort":1,
   "data":"MjMuMzc1"
} """

# ajouter la lib paho : pip install paho
import paho.mqtt.client as mqtt
import json
import base64
import logging

# config
mqttServer = "localhost"
appID = "5"
deviceID = "010203040506070b"

# du log pour debug
logging.basicConfig(level=logging.DEBUG)

# callback appele lors de la reception d un message


def on_message(mqttc, obj, msg):
    # {'applicationID': '5', 'applicationName': 'RB-home', 'deviceName': 'RB-feather-M0',
    # 'devEUI': '010203040506070b', 'rxInfo': [{'gatewayID': '3150000000000002', 'name':
    # 'toulouse_remi', 'rssi': -96, 'loRaSNR': 6.2, 'location': {'latitude': 43.60625069174644,
    # 'longitude': 1.4709877967834475, 'altitude': 204}}], 'txInfo': {'frequency': 868300000,
    # 'dr': 5}, 'adr': True, 'fCnt': 58, 'fPort': 1, 'data': 'MjMuMzc1'}

    jsonMsg = json.loads(msg.payload)
    # print(msg.payload)
    device = jsonMsg["devEUI"]
    gw = jsonMsg["rxInfo"][0]["gatewayID"]
    rssi = jsonMsg["rxInfo"][0]["rssi"]
    loRaSNR = jsonMsg["rxInfo"][0]["loRaSNR"]
    latitude = jsonMsg["rxInfo"][0]["location"]["latitude"]
    longitude = jsonMsg["rxInfo"][0]["location"]["longitude"]
    altitude = jsonMsg["rxInfo"][0]["location"]["altitude"]
    frequency = jsonMsg["txInfo"]["frequency"]
    data = base64.b64decode(jsonMsg["data"])
    print()
    print("Dev ID : " + device + ", Gateway ID : " + gw + ", RSSI : "+str(rssi) + ", LoRaSNR : "+str(loRaSNR) + ", Data : " +
          data.decode())
    print()
    print("Dev ID : " + device + "\nGateway ID : " + gw + "\nRSSI : "+str(rssi) + "\nLoRaSNR : "+str(loRaSNR) +"\nfrequency : "+str(frequency)+"\nLatitude : "+str(latitude)+"\nlongitude : "+str(longitude)+"\naltitude : "+str(altitude) + "\nData : " +
          data.decode())


# creation du client
mqttc = mqtt.Client()

mqttc.on_message = on_message

logger = logging.getLogger(__name__)

mqttc.enable_logger(logger)

mqttc.connect(mqttServer, 1883, 60)

# soucription au device
mqttc.subscribe("application/"+appID+"/device/"+deviceID+"/rx", 0)

mqttc.loop_forever()
