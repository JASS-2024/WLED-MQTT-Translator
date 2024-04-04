import paho.mqtt.client as mqtt
import websocket
import threading

from datetime import datetime

BROKER_ADDRESS = "192.168.3.85"
BROKER_PORT = 1883
# WLED_WS_ADDRESS = "ws://192.168.0.48/ws"
WLED_WS_ADDRESS = "ws://192.168.0.33/ws"
TOPIC = "WLEDTranslator/48"


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_open(ws):
    mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    ws.send("{'lv':true}")

def on_close(ws):
    mqtt_client.disconnect()
    print("WebSocket connection closed")

def forward_message(ws, message):
    mqtt_client.publish(TOPIC, message)

ws = websocket.WebSocketApp(WLED_WS_ADDRESS, on_message=forward_message, on_open=on_open, on_close=on_close)
while True:
    ws.run_forever()