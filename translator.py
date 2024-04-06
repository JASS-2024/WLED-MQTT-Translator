import paho.mqtt.client as mqtt
import websocket
import threading
import time

BROKER_ADDRESS = "192.168.3.85"
BROKER_PORT = 1883
WLED_IP_ADDRESSES = ["192.168.0.48", "192.168.0.33", "192.168.0.52", "192.168.1.156"] 
BASE_TOPIC = "WLEDTranslator/"
DELAY_BEFORE_RESTART = 5

last_messages = {}

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)
mqtt_client.loop_start()

def on_open(ws):
    def retrieve_stream():
        # We keep asking for the stream in case someone else stole it!
        while True:
            ws.send("{'lv':true}")
            time.sleep(DELAY_BEFORE_RESTART)
    t = threading.Thread(target=retrieve_stream)
    t.start()

def on_close(ws):
    print("WebSocket connection closed")

def forward_message(ws, message):
    print(f"forwarding {ws.mqtt_topic}")
    mqtt_client.publish(ws.mqtt_topic, message, 1)

def forward_from_ip(ip):
    ws = websocket.WebSocketApp(f"ws://{ip}/ws", on_message=forward_message, on_open=on_open, on_close=on_close)
    ws.mqtt_topic = BASE_TOPIC + ip.rsplit(".")[-1]
    ws.run_forever(reconnect=True)

for ip in WLED_IP_ADDRESSES:
    t = threading.Thread(target=lambda :forward_from_ip(ip) )
    t.start()
