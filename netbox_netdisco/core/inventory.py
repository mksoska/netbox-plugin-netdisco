from .netdisco import Netdisco
from .icinga2 import Icinga
from .models import initialize, clear_all
from netbox import settings


class Inventory():
    # Later add support for AsyncResult (maybe even HTTPResponse) returned from any get method of models

    @staticmethod
    def collect(**kwargs):
        with Netdisco(settings.PLUGINS_CONFIG.get("netbox_netdisco")):
            clear_all()
            initialize(**kwargs)
    
            

    #TODO: Send inconsistencies notification to Icinga
    @staticmethod
    def notify_inconsistecies():
        pass
