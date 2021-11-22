from openapi_netdisco.rest import ApiException 
from openapi_netdisco import Configuration, ApiClient, GeneralApi

class Client():
    # Add exception handling if <required_settings> in NetBox's 
    # <configuration.py> not working as expected    
    def __init__(self, client_config):       
        self.configuration = Configuration(
            host=client_config.get("NETDISCO_HOST"),
            username=client_config.get("NETDISCO_USERNAME"),
            password=client_config.get("NETDISCO_PASSWORD")
        )
            
    def __enter__(self):
        self.api_client = ApiClient(self.configuration).__enter__()
        self.general_api = GeneralApi(self.api_client)

        self.login()        

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()

        self.api_client.__exit__(exc_type, exc_value, traceback)


    def login(self):
        try:
            self.configuration.api_key["APIKeyHeader"] = self.general_api.login_post().api_key
        except ApiException as e:
            print("Exception when calling GeneralApi->login_post: %s\n" % e)

    def logout(self):
        try:
            self.general_api.logout_get()
        except ApiException as e:
            print("Exception when calling GeneralApi->logout_get: %s\n" % e)

