import paho.mqtt.client as mqtt
import websocket
import threading

BROKER_ADDRESS = "192.168.3.85"
BROKER_PORT = 1883
WLED_IP_ADDRESSES = ["192.168.0.33", "192.168.0.48"]
BASE_TOPIC = "WLEDTranslator/"


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_open(ws):
    mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
    ws.send("{'lv':true}")

def on_close(ws):
    mqtt_client.disconnect()
    print("WebSocket connection closed")

def forward_message(ws, message):
    print(ws.mqtt_topic)
    mqtt_client.publish(ws.mqtt_topic, message)

def forward_from_ip(ip):
    ws = websocket.WebSocketApp(f"ws://{ip}/ws", on_message=forward_message, on_open=on_open, on_close=on_close)
    ws.mqtt_topic = BASE_TOPIC + ip.rsplit(".")[-1]
    while True:
        ws.run_forever()

for ip in WLED_IP_ADDRESSES:
    t = threading.Thread(target=lambda :forward_from_ip(ip) )
    t.start()
