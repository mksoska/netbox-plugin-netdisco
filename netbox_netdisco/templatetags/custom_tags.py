from django import template

register = template.Library()


@register.simple_tag
def getdict_netdisco(model):
    return model.netdisco.to_dict()

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
def getattr_verbose(model, key):
    return model.attrs.getattr_verbose(key)