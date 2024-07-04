# python 3.11
import time
from paho.mqtt import client as mqtt_client

broker = "192.168.0.108"
port = 1883
topic = "mqtt/rpi/image"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    image_path = "gep.jpg"
    start_time = time.time()
    client.publish(topic, image_path, qos=1).wait_for_publish()
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken to publish: {time_taken:.2f} seconds")

def run():
    client = connect_mqtt()
    publish(client)
    client.disconnect()

if __name__ == '__main__':
    run()