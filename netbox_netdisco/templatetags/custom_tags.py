from django import template
from netbox import settings

register = template.Library()


@register.simple_tag
def getattr_netdisco(model, key):
    return model.attrs.getattr_netdisco(key)

@register.simple_tag
def getattr_netbox(model, key):
    return model.attrs.getattr_netbox(key)

@register.simple_tag
def attr_consistent(model, key):
    return model.attrs.attr_consistent(key)

@register.simple_tag
def attr_ignore(model, key):
    return key in model.tables["INGORE"]

@register.simple_tag
def getattr_verbose(model, key):
    return model.attrs.getattr_verbose(key)

@register.simple_tag
def gethost_netdisco():
    host = settings.PLUGINS_CONFIG.get("netbox_netdisco", {}).get("NETDISCO_HOST")
    return host if host[len(host) - 1] == '/' else host + '/'