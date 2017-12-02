from django.conf import settings
import warnings
from importlib import import_module
import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep


class MQTT:

    def __init__(self):
        if not hasattr(settings, 'INSTALLED_MQTT_APPS') or  not hasattr(settings, 'MQTT_SETTINGS'):
            warnings.warn("No mqtt apps or settings found in the global settings. "
                          "Are you sure you do not want an API?",
                          RuntimeWarning, stacklevel=2)

        self.mqtt_client = mqtt.Client(client_id=settings.MQTT_SETTINGS["CLIENT_ID"],
                                       clean_session=settings.MQTT_SETTINGS["CLEAN_SESSION"], userdata=None)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.username_pw_set(settings.MQTT_SETTINGS["USERNAME"], password=settings.MQTT_SETTINGS["PASSW"])

        self.topics = {}
        self.trhead = None
        self.want_disconnect = False
        for mqtt_app in settings.INSTALLED_MQTT_APPS:
            self.append_module_mqtt(mqtt_app)

        self.mqtt_client.connect(settings.MQTT_SETTINGS["IP"], settings.MQTT_SETTINGS["PORT"], 60)

    def on_connect(self, client, userdata, flags, rc):
        print("MQTT - Connected with result code " + str(rc))
        for topic in self.topics:
            client.subscribe(topic, qos=0)
            print("MQTT - subscribed " + topic + " as topc")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        for topic in self.topics:
            if topic == msg.topic:
                self.topics[topic](self, userdata, msg)
        #message_callback_add(sub, callback)

    def publish(self, topic, payload=None, retain=False):
        self.mqtt_client.publish(topic, payload=payload, qos=0, retain=retain)

    def start_listening(self):

        self.thread = Thread(target=self.mqtt_client.loop_start)
        self.thread.start()

    def stop_listening(self):
        self.mqtt_client.loop_stop(force=False)


    def close(self):
        self.want_disconnect=True
        self.mqtt_client.disconnect()

    def append_module_mqtt(self, mqtt_app):
        # Try and import the base module
        try:
            module_topics = import_module(mqtt_app + "mqtt")
            if not hasattr(module_topics, 'TOPICS'):
                return
            for topic in module_topics.TOPIC:
                self.topics[topic] = module_topics.TOPIC[topic]


        except ImportError:
            raise RuntimeError("API module %s could not be imported" % mqtt_app)

    def unsubscribe(self, topic):
        self.mqtt_client.unsubscribe(topic)

    def on_disconnect(self, client, userdata, rc):
        print("MTQQ - disconected")
        if not self.want_disconnect:
            sleep(10)
            print("MTQQ - trying to reconnect")
            self.mqtt_client.loop_start()
