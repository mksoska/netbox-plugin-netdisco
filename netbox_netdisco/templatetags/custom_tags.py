from django import template

register = template.Library()

@register.simple_tag
def getattr_netdisco(model, key):
    return model.getattr_netdisco(key)

@register.simple_tag
def getattr_netbox(model, key):
    return model.getattr_netbox(key)

@register.simple_tag
def getattr_name(model, key):
    return model.attribute_tag[key]