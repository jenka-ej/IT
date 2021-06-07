# subscriber.py

import paho.mqtt.client as mqtt
import time
from queue import Queue
def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("message received ", str(message.payload.decode("utf-8")), flush=True)
    print("message topic=", message.topic, flush=True)
    q.put(data)

# Подключение к брокеру

q = Queue()
time.sleep(25)
client_2 = mqtt.Client("default_2")
client_2.on_message = on_message
client_2.connect("127.0.0.1", 1883, 60)
client_2.loop_start()
print('Подключен')
client_2.subscribe('sensors/humidity')
while True:
    time.sleep(4)
    client_2.on_message = on_message
    while not q.empty():
        message = q.get()
        if message is None:
            continue
        value = float(message)
        if value < 30:
            client_2.publish("humidifier", 'ON')
        elif value > 60:
                client_2.publish("humidifier", 'OFF')
        print("received from queue", message, flush=True)
    time.sleep(4)

# publisher.py

import paho.mqtt.client as mqtt
import time
from random import uniform
from queue import Queue
def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("message received ", str(message.payload.decode("utf-8")), flush=True)
    print("message topic=", message.topic, flush=True)
    q.put(data)

# Подключение к брокеру

q = Queue()
client = mqtt.Client("default")  # Создание клиента
print("Подключение к брокеру")
client.connect("127.0.0.1", 1883, 60)  # Подключение к брокеру
client.loop_start()
print("Отправка сообщений в топик", "sensors")
while True:
    humidity_value = uniform(10.0, 70.0)    # Создание псевдослучайных значений влажности
    client.publish("sensors/humidity", humidity_value)    # Отправка данных значений
    client.subscribe("humidifier")
    client.on_message = on_message
    time.sleep(4)
