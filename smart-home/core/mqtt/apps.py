from django.apps import AppConfig
from .mqtt import MQTT


class MqttConfig(AppConfig):
    name = 'mqtt'
    mqtt = None

    def ready(self):
        super().ready()
        self.mqtt = MQTT()


def publish(topic, payload=None, retain=False):
    MqttConfig.mqtt.publish(topic, payload=payload, retain=retain)
