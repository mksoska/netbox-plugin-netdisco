from openapi_netdisco import ReportsApi, SearchApi, ObjectsApi
from .client import Client


class Netdisco():    
    def __enter__(self):
        self.client = Client().__enter__()
        Netdisco.objects = ObjectsApi(self.client.api_client)
        Netdisco.search = SearchApi(self.client.api_client)
        Netdisco.reports = ReportsApi(self.client.api_client) 
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.__exit__(exc_type, exc_value, traceback)
        


