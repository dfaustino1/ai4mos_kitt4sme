from fipy.docker import DockerCompose
from tests.util.fiware import wait_on_orion, create_subscriptions
from tests.util.sampler import ProductionSampler 
import paho.mqtt.client as mqtt
import json
from fipy.ngsi.orion import OrionClient
from tests.util.fiware import orion_client


docker = DockerCompose(__file__)
entity_id = 1


def bootstrap():
    docker.build_images()
    docker.start()
    
    wait_on_orion()
    
    create_subscriptions()


def send_machine_entities(json_data, id):
    samplerProduction = ProductionSampler(orion_client(),json_data, id)
    try:
        samplerProduction.insert_entity()
    except Exception as e:
        print(e)


def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    global entity_id
    send_machine_entities(data,entity_id)
    entity_id += 1


def run():
    services_running = False
    try:
        bootstrap()
        services_running = True
        print('>>> sending machine entities to Orion...')
        
        # Subscribing to an mqtt broker to get data from our source
        client = mqtt.Client()
        client.on_message = on_message
        client.connect("test.mosquitto.org", 1883)
        client.subscribe("kitt4sme")
        client.loop_start()
        while True:
            pass
    except KeyboardInterrupt:
        if services_running:
            docker.stop()
            