
import json

# from numpy import isin
# from orsim.config import settings
import requests
# import urllib3
# from urllib.parse import quote
import logging

import paho.mqtt.client as paho


class Messenger:

    def __init__(self, settings, credentials, channel_id=None, on_message=None, transport=None):
        ''' '''
        self.settings = settings
        self.credentials = credentials
        self.channel_id = channel_id

        if transport is None:
            self.client = paho.Client(credentials['email'],  clean_session=True)
            self.client.username_pw_set(username=self.credentials['email'], password=self.credentials['password'])
            # Messenger.register_user(self.credentials['email'], self.credentials['password'])
            self.register_user(self.credentials['email'], self.credentials['password'])

            self.client.connect(self.settings['MQTT_BROKER'])

        if on_message is not None:
            self.client.on_message = on_message


        # RabbitMQ PubSub queue is used for processing requests in sequence
        # This is a deliberate design choice to enable:
        #   - Inter-Agent communication as core part of system design

        # if channel_id is not None:
        if isinstance(channel_id, str):
            # self.client.loop_start()
            self.client.subscribe(channel_id, qos=0)
            logging.debug(f"Channel: {channel_id}")
        elif isinstance(channel_id, list):
            # self.client.loop_start()
            self.client.subscribe([(cid, 0) for cid in channel_id])
            logging.debug(f"Channel: {channel_id}")

        self.client.loop_start()



    def disconnect(self):
        ''' '''
        # try:
        #     self.client.unsubscribe(self.channel_id)
        # except Exception as e:
        #     logging.exception(str(e))

        if self.channel_id is not None:
            try:
                self.client.loop_stop(force=True)
            except Exception as e:
                logging.exception(str(e))

        try:
            self.client.disconnect()
        except Exception as e:
            logging.exception(str(e))




    # @classmethod
    def register_user(self, username, password):
        ''' '''

        response = requests.get(f"{self.settings['RABBITMQ_MANAGEMENT_SERVER']}/users/{username}")
        if (response.status_code >= 200) and (response.status_code <= 299):
            logging.warning('User is already registered')
        else:
            try:
                response = requests.put(f"{self.settings['RABBITMQ_MANAGEMENT_SERVER']}/users/{username}",
                                        data=json.dumps({'password': password, 'tags': ''}),
                                        headers={"content-type": "application/json"},
                                        auth=(self.settings['RABBITMQ_ADMIN_USER'], self.settings['RABBITMQ_ADMIN_PASSWORD'])
                                    )
            except Exception as e:
                logging.exception(str(e))
                raise e

        # reset the user and set appropriate permissions as needed
        quoted_slash = '%2F'
        response = requests.put(f"{self.settings['RABBITMQ_MANAGEMENT_SERVER']}/permissions/{quoted_slash}/{username}",
                        data=json.dumps({"username":username, "vhost":"/", "configure":".*", "write":".*", "read":".*"}),
                        headers={"content-type": "application/json"},
                        auth=(self.settings['RABBITMQ_ADMIN_USER'], self.settings['RABBITMQ_ADMIN_PASSWORD'])
                    )

        response = requests.put(f"{self.settings['RABBITMQ_MANAGEMENT_SERVER']}/topic-permissions/{quoted_slash}/{username}",
                        data=json.dumps({username: username, "vhost": "/", "exchange": "", "write": ".*", "read": ".*"}),
                        headers={"content-type": "application/json"},
                        auth=(self.settings['RABBITMQ_ADMIN_USER'], self.settings['RABBITMQ_ADMIN_PASSWORD'])
                    )

