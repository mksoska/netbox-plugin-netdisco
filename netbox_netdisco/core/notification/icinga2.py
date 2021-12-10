import requests
import json

class Icinga():
    def __init__(self, client_configuration):
        self.host = client_configuration.get("ICINGA2_HOST")
        self.username = client_configuration.get("ICINGA2_USERNAME")
        self.password = client_configuration.get("ICINGA2_PASSWORD")

    def send(self, comment):
        headers = {
            'Accept': 'application/json',
            'X-HTTP-Method-Override': 'POST'
        }

        data = {
            "type": "Service",
            "author": "Netbox Plugin Netdisco",
            "comment": comment,
            "force": True,
            "pretty": True
        }

        request_url = self.host + "/v1/actions/send-custom-notification"

        return requests.post(
            request_url,
            headers=headers,
            auth=(self.username, self.password),
            data=json.dumps(data),
            verify=False
        )        

        


