import paho.mqtt.client as mqttc
import paho.mqtt.properties as properties
import paho.mqtt.packettypes as packettypes

HOST = "broker.hivemq.com"
PORT = 1883
TOPIC_PREFIX = "hspf/"
CHATTER_TOPIC = TOPIC_PREFIX+"chatroom"
NAME = "OKY"


def on_message(client:mqttc.Client,userdata,msg:mqttc.MQTTMessage):
    payload = msg.payload.decode('utf-8')
    username = "Unknown"
    if hasattr(msg.properties, "UserProperty") and msg.properties.UserProperty:
        username = msg.properties.UserProperty[0][1]
    print(username + ": "+ payload)

client = mqttc.Client(protocol=mqttc.MQTTv5)
props = properties.Properties(packettypes.PacketTypes.PUBLISH)
props.UserProperty = ("name",NAME)

client.on_message = on_message
client.connect(HOST,PORT)
client.subscribe(CHATTER_TOPIC)
client.loop_start()
print("Now starting")

while True:
    try:
        message = input()
        client.publish(
            CHATTER_TOPIC,
            payload=message,
            qos=2,
            properties=props
        )
    except KeyboardInterrupt:
        break

print("Now exiting")