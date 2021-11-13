from openapi_netdisco import ReportsApi
from openapi_netdisco import SearchApi
from openapi_netdisco import ObjectsApi
from .client import Client


class Netdisco():
    #Maybe do as context manager
    @classmethod
    def start_session(cls):
        cls.client = Client().__enter__()
        cls.objects = ObjectsApi(cls.client)
        cls.search = SearchApi(cls.client)
        cls.reports = ReportsApi(cls.client)  

    @classmethod
    def close(cls):
        cls.client.__exit__()

Netdisco.start_session()
