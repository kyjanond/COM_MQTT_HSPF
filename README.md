# MQTT workshop HSPF
This is a repository for a M2M MQTT workshop at the MADFM - Hochschule Pforzheim.

## Dependencies
- [pygame](https://pypi.org/project/pygame/)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/)
## Required external apps
- Android app
  - [Sensor Node Free](https://play.google.com/store/apps/details?id=com.mscino.sensornode&hl=en&gl=US)
  - messages are encoded as BASE_TOPIC/SENSOR/DATA => value as a primitive type (e.g. mytopic/Accelerometer/x => 0.89766)

- iPhone app
  - [Cedalo MQTT Connect](https://apps.apple.com/us/app/cedalo-mqtt-connect/id1462295012)
  - messages are encoded as BASE_TOPIC => json data (see dev/iphone_msg.json)
  - example data in [iphone_msg_example.json](./dev/iphone_msg_example.json).

