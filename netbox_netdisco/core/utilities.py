
from netbox_netdisco.templatetags.custom_tags import attr_consistent


def sum_inconsistent(models):
    return sum(1 for model in models if not model.is_consistent)    


def merge_dicts(*args):
    result = {}
    for dict_ in args:
        result.update(dict_)
    return result


def get_orm(orm_map, model_netdisco, queryset):
    query = {orm_map[key]: getattr(model_netdisco, key) for key in orm_map} if orm_map else None
    return queryset.filter(**query).first() if query else None


class AttributeResolve():
    def __init__(self, netdisco, netbox, netdisco_attr, netbox_attr, verbose_attr, ignore_attr):
        self.netdisco = netdisco
        self.netbox = netbox
        self.netdisco_attr = netdisco_attr
        self.netbox_attr = netbox_attr
        self.verbose_attr = verbose_attr
        self.ignore_attr = ignore_attr

    def getattr_netdisco(self, key):
        unmangled = key.rstrip('_')
        lambda_ = self.netdisco_attr.get(unmangled, lambda x: getattr(x, unmangled))
        try:
            return lambda_(self.netdisco)
        except AttributeError:
            return None
        #return self._getattr_generic("self.netdisco.", unmangled, self.netdisco_attr_convert.get(key, lambda x: x))

    def getattr_netbox(self, key):
        unmangled = key.rstrip('_')
        lambda_ = self.netbox_attr.get(unmangled, lambda x: str(getattr(x, unmangled)))
        try:
            return lambda_(self.netbox)
        except AttributeError:
            return None
        #return self._getattr_generic("self.netbox.", self.attribute_map.get(key), self.netbox_attr_convert.get(key, lambda x: str(x)))
        
    def getattr_verbose(self, key):
        verbose = self.verbose_attr.get(key)
        return verbose if verbose else key.capitalize()

    def attr_consistent(self, key):    
        if self.getattr_netdisco(key) == self.getattr_netbox(key):
            return True
        return None if key in self.ignore_attr else False
